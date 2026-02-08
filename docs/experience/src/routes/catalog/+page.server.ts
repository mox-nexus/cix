import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';
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
		// Strip leading > for blockquote taglines
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

function loadPlugins(): CatalogExtension[] {
	const marketplacePath = join(PLUGINS_DIR, '.claude-plugin', 'marketplace.json');
	if (!existsSync(marketplacePath)) return [];

	const marketplace = JSON.parse(readFileSync(marketplacePath, 'utf-8'));
	const publishedNames = new Set(
		marketplace.plugins.map((p: { name: string }) => p.name)
	);

	const extensions: CatalogExtension[] = [];

	for (const entry of readdirSync(PLUGINS_DIR)) {
		if (!publishedNames.has(entry)) continue;

		const pluginDir = join(PLUGINS_DIR, entry);
		if (!statSync(pluginDir).isDirectory()) continue;

		const manifestPath = join(pluginDir, '.claude-plugin', 'plugin.json');
		if (!existsSync(manifestPath)) continue;

		const manifest: PluginManifest = JSON.parse(readFileSync(manifestPath, 'utf-8'));
		const readmePath = join(pluginDir, 'README.md');
		const readme = existsSync(readmePath) ? readFileSync(readmePath, 'utf-8') : '';

		extensions.push({
			slug: manifest.name,
			kind: 'plugin',
			manifest,
			tagline: extractTagline(readme),
			readme,
			components: discoverComponents(pluginDir),
			variant: VARIANTS[extensions.length % VARIANTS.length],
			tags: manifest.keywords ?? []
		});
	}

	return extensions;
}

function loadTools(): CatalogExtension[] {
	const marketplacePath = join(TOOLS_DIR, '.claude-plugin', 'marketplace.json');
	if (!existsSync(marketplacePath)) return [];

	const marketplace = JSON.parse(readFileSync(marketplacePath, 'utf-8'));
	const toolEntries: Array<{ name: string; description: string }> = marketplace.tools ?? [];

	const extensions: CatalogExtension[] = [];

	for (const tool of toolEntries) {
		const toolDir = join(TOOLS_DIR, tool.name);
		if (!existsSync(toolDir) || !statSync(toolDir).isDirectory()) continue;

		const readmePath = join(toolDir, 'README.md');
		const readme = existsSync(readmePath) ? readFileSync(readmePath, 'utf-8') : '';

		// Read version from pyproject.toml if available
		const pyprojectPath = join(toolDir, 'pyproject.toml');
		let version = '0.1.0';
		if (existsSync(pyprojectPath)) {
			const pyproject = readFileSync(pyprojectPath, 'utf-8');
			const versionMatch = pyproject.match(/^version\s*=\s*"([^"]+)"/m);
			if (versionMatch) version = versionMatch[1];
		}

		extensions.push({
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
			variant: VARIANTS[extensions.length % VARIANTS.length],
			tags: ['tool', 'cli']
		});
	}

	return extensions;
}

export const load: PageServerLoad = async () => {
	const plugins = loadPlugins();
	const tools = loadTools();
	const extensions = [...plugins, ...tools].sort((a, b) => a.slug.localeCompare(b.slug));

	return { extensions };
};
