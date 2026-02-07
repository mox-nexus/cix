import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import type { CatalogPlugin, PluginManifest, PluginComponents } from '$lib/types/catalog';
import { CATALOG_NARRATIVES } from '$lib/data/catalog-narratives';

const PLUGINS_DIR = resolve(process.cwd(), '../../plugins');
const VARIANTS = ['spark', 'emergence', 'constraint'] as const;

function countFiles(dir: string, extension = '.md'): number {
	if (!existsSync(dir)) return 0;
	return readdirSync(dir).filter((f) => f.endsWith(extension)).length;
}

function countDirs(dir: string): number {
	if (!existsSync(dir)) return 0;
	return readdirSync(dir).filter((f) => statSync(join(dir, f)).isDirectory()).length;
}

function discoverComponents(pluginDir: string): PluginComponents {
	return {
		agents: countFiles(join(pluginDir, 'agents')),
		skills: countDirs(join(pluginDir, 'skills')),
		hooks: countFiles(join(pluginDir, 'hooks'), '.sh'),
		commands: countDirs(join(pluginDir, 'commands'))
	};
}

export const load: PageServerLoad = async ({ params }) => {
	const { slug } = params;

	const marketplacePath = join(PLUGINS_DIR, '.claude-plugin', 'marketplace.json');
	const marketplace = JSON.parse(readFileSync(marketplacePath, 'utf-8'));
	const publishedNames = new Set(
		marketplace.plugins.map((p: { name: string }) => p.name)
	);

	if (!publishedNames.has(slug)) {
		throw error(404, `Extension not found: ${slug}`);
	}

	const pluginDir = join(PLUGINS_DIR, slug);
	if (!existsSync(pluginDir) || !statSync(pluginDir).isDirectory()) {
		throw error(404, `Extension not found: ${slug}`);
	}

	const manifestPath = join(pluginDir, '.claude-plugin', 'plugin.json');
	if (!existsSync(manifestPath)) {
		throw error(404, `Extension not found: ${slug}`);
	}

	const manifest: PluginManifest = JSON.parse(readFileSync(manifestPath, 'utf-8'));
	const readmePath = join(pluginDir, 'README.md');
	const readme = existsSync(readmePath) ? readFileSync(readmePath, 'utf-8') : '';

	// Determine variant index from sorted position
	const allPublished = Array.from(publishedNames).sort();
	const variantIndex = allPublished.indexOf(slug);
	const narrative = CATALOG_NARRATIVES[slug];

	const plugin: CatalogPlugin = {
		slug: manifest.name,
		manifest,
		tagline: '',
		readme,
		components: discoverComponents(pluginDir),
		variant: VARIANTS[variantIndex % VARIANTS.length],
		narrativeHook: narrative?.narrativeHook,
		constraint: narrative?.constraint
	};

	return { plugin };
};
