import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import type {
	CatalogExtension,
	PluginManifest,
	PluginComponents,
	ExtensionDocs,
	DocCategory,
	DocEntry
} from '$lib/types/catalog';

const ROOT_DIR = resolve(process.cwd(), '../..');
const PLUGINS_DIR = join(ROOT_DIR, 'plugins');
const TOOLS_DIR = join(ROOT_DIR, 'tools');
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

const DOC_CATEGORIES: DocCategory[] = ['explanation', 'how-to', 'tutorials'];

function extractTitle(content: string): string {
	for (const line of content.split('\n')) {
		if (line.startsWith('# ')) return line.slice(2).trim();
	}
	return '';
}

function discoverDocs(dir: string): ExtensionDocs {
	const docs: ExtensionDocs = { explanation: [], 'how-to': [], tutorials: [] };
	const docsDir = join(dir, 'docs');
	if (!existsSync(docsDir)) return docs;

	for (const category of DOC_CATEGORIES) {
		const categoryDir = join(docsDir, category);
		if (!existsSync(categoryDir)) continue;

		for (const file of readdirSync(categoryDir).filter((f) => f.endsWith('.md')).sort()) {
			const content = readFileSync(join(categoryDir, file), 'utf-8');
			docs[category].push({
				slug: file.replace(/\.md$/, ''),
				title: extractTitle(content) || file.replace(/\.md$/, ''),
				content
			});
		}
	}

	return docs;
}

function countDocEntries(docs: ExtensionDocs): number {
	return docs.explanation.length + docs['how-to'].length + docs.tutorials.length;
}

function tryLoadPlugin(slug: string): CatalogExtension | null {
	const marketplacePath = join(ROOT_DIR, '.claude-plugin', 'marketplace.json');
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
	const docs = discoverDocs(pluginDir);

	return {
		slug: manifest.name,
		kind: 'plugin',
		manifest,
		tagline: extractTagline(readme),
		readme,
		components: discoverComponents(pluginDir),
		variant: VARIANTS[variantIndex % VARIANTS.length],
		tags: manifest.keywords ?? [],
		docs,
		docCount: countDocEntries(docs)
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

	const docs = discoverDocs(toolDir);

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
		tags: ['tool', 'cli'],
		docs,
		docCount: countDocEntries(docs)
	};
}

export function entries() {
	const slugs: Array<{ slug: string }> = [];

	const pluginMarketplace = join(ROOT_DIR, '.claude-plugin', 'marketplace.json');
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
