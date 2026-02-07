import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';
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

function extractTagline(readme: string): string {
	const lines = readme.split('\n');
	let foundH1 = false;
	for (const line of lines) {
		if (line.startsWith('# ')) {
			foundH1 = true;
			continue;
		}
		if (!foundH1) continue;
		const trimmed = line.trim();
		if (trimmed === '') continue;
		if (trimmed.startsWith('#')) break;
		return trimmed;
	}
	return '';
}

function discoverComponents(pluginDir: string): PluginComponents {
	return {
		agents: countFiles(join(pluginDir, 'agents')),
		skills: countDirs(join(pluginDir, 'skills')),
		hooks: countFiles(join(pluginDir, 'hooks'), '.sh'),
		commands: countDirs(join(pluginDir, 'commands'))
	};
}

export const load: PageServerLoad = async () => {
	const marketplacePath = join(PLUGINS_DIR, '.claude-plugin', 'marketplace.json');
	const marketplace = JSON.parse(readFileSync(marketplacePath, 'utf-8'));
	const publishedNames = new Set(
		marketplace.plugins.map((p: { name: string }) => p.name)
	);

	const plugins: CatalogPlugin[] = [];

	for (const entry of readdirSync(PLUGINS_DIR)) {
		if (!publishedNames.has(entry)) continue;

		const pluginDir = join(PLUGINS_DIR, entry);
		if (!statSync(pluginDir).isDirectory()) continue;

		const manifestPath = join(pluginDir, '.claude-plugin', 'plugin.json');
		if (!existsSync(manifestPath)) continue;

		const manifest: PluginManifest = JSON.parse(readFileSync(manifestPath, 'utf-8'));
		const readmePath = join(pluginDir, 'README.md');
		const readme = existsSync(readmePath) ? readFileSync(readmePath, 'utf-8') : '';
		const narrative = CATALOG_NARRATIVES[manifest.name];

		plugins.push({
			slug: manifest.name,
			manifest,
			tagline: extractTagline(readme),
			readme,
			components: discoverComponents(pluginDir),
			variant: VARIANTS[plugins.length % VARIANTS.length],
			narrativeHook: narrative?.narrativeHook,
			constraint: narrative?.constraint
		});
	}

	plugins.sort((a, b) => a.slug.localeCompare(b.slug));

	return { plugins };
};
