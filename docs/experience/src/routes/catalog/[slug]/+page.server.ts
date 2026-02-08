import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import type { CatalogExtension, PluginManifest, PluginComponents } from '$lib/types/catalog';

const PLUGINS_DIR = resolve(process.cwd(), '../../plugins');
const TOOLS_DIR = resolve(process.cwd(), '../../tools');
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
		return trimmed.replace(/^>\s*/, '');
	}
	return '';
}

function discoverComponents(dir: string): PluginComponents {
	return {
		agents: countFiles(join(dir, 'agents')),
		skills: countDirs(join(dir, 'skills')),
		hooks: countFiles(join(dir, 'hooks'), '.sh'),
		commands: countDirs(join(dir, 'commands'))
	};
}

function tryLoadPlugin(slug: string): CatalogExtension | null {
	const marketplacePath = join(PLUGINS_DIR, '.claude-plugin', 'marketplace.json');
	if (!existsSync(marketplacePath)) return null;

	const marketplace = JSON.parse(readFileSync(marketplacePath, 'utf-8'));
	const publishedNames = new Set(
		marketplace.plugins.map((p: { name: string }) => p.name)
	);

	if (!publishedNames.has(slug)) return null;

	const pluginDir = join(PLUGINS_DIR, slug);
	if (!existsSync(pluginDir) || !statSync(pluginDir).isDirectory()) return null;

	const manifestPath = join(pluginDir, '.claude-plugin', 'plugin.json');
	if (!existsSync(manifestPath)) return null;

	const manifest: PluginManifest = JSON.parse(readFileSync(manifestPath, 'utf-8'));
	const readmePath = join(pluginDir, 'README.md');
	const readme = existsSync(readmePath) ? readFileSync(readmePath, 'utf-8') : '';

	const allPublished = Array.from(publishedNames).sort();
	const variantIndex = allPublished.indexOf(slug);

	return {
		slug: manifest.name,
		kind: 'plugin',
		manifest,
		tagline: extractTagline(readme),
		readme,
		components: discoverComponents(pluginDir),
		variant: VARIANTS[variantIndex % VARIANTS.length],
		tags: manifest.keywords ?? []
	};
}

function tryLoadTool(slug: string): CatalogExtension | null {
	const marketplacePath = join(TOOLS_DIR, '.claude-plugin', 'marketplace.json');
	if (!existsSync(marketplacePath)) return null;

	const marketplace = JSON.parse(readFileSync(marketplacePath, 'utf-8'));
	const toolEntries: Array<{ name: string; description: string }> =
		marketplace.tools ?? [];
	const tool = toolEntries.find((t) => t.name === slug);
	if (!tool) return null;

	const toolDir = join(TOOLS_DIR, slug);
	if (!existsSync(toolDir) || !statSync(toolDir).isDirectory()) return null;

	const readmePath = join(toolDir, 'README.md');
	const readme = existsSync(readmePath) ? readFileSync(readmePath, 'utf-8') : '';

	let version = '0.1.0';
	const pyprojectPath = join(toolDir, 'pyproject.toml');
	if (existsSync(pyprojectPath)) {
		const pyproject = readFileSync(pyprojectPath, 'utf-8');
		const versionMatch = pyproject.match(/^version\s*=\s*"([^"]+)"/m);
		if (versionMatch) version = versionMatch[1];
	}

	return {
		slug: tool.name,
		kind: 'tool',
		manifest: {
			name: tool.name,
			version,
			description: tool.description,
			author: { name: 'Mox Labs' }
		},
		tagline: extractTagline(readme),
		readme,
		components: discoverComponents(toolDir),
		variant: VARIANTS[0],
		tags: ['tool', 'cli']
	};
}

export function entries() {
	const slugs: Array<{ slug: string }> = [];

	const pluginMarketplace = join(PLUGINS_DIR, '.claude-plugin', 'marketplace.json');
	if (existsSync(pluginMarketplace)) {
		const mp = JSON.parse(readFileSync(pluginMarketplace, 'utf-8'));
		for (const p of mp.plugins ?? []) {
			slugs.push({ slug: p.name });
		}
	}

	const toolMarketplace = join(TOOLS_DIR, '.claude-plugin', 'marketplace.json');
	if (existsSync(toolMarketplace)) {
		const mp = JSON.parse(readFileSync(toolMarketplace, 'utf-8'));
		for (const t of mp.tools ?? []) {
			slugs.push({ slug: t.name });
		}
	}

	return slugs;
}

export const load: PageServerLoad = async ({ params }) => {
	const { slug } = params;

	const extension = tryLoadPlugin(slug) ?? tryLoadTool(slug);
	if (!extension) {
		throw error(404, `Extension not found: ${slug}`);
	}

	return { extension };
};
