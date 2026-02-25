import { error } from '@sveltejs/kit';
import { getEntry, getNavigation } from './docs';

/**
 * Load markdown content for a docs article.
 *
 * Uses Vite's import.meta.glob so the bundler can resolve all content
 * at build time. The slug selects the file at runtime.
 */
export async function loadDocsContent(slug: string) {
	const entry = getEntry(slug);
	if (!entry) {
		throw error(404, `Not found: ${slug}`);
	}

	const filename = entry.file ?? slug;
	const modules = import.meta.glob('../../../../content/docs/**/*.md', {
		query: '?raw',
		import: 'default',
		eager: true
	}) as Record<string, string>;
	const path = `../../../../content/docs/${filename}.md`;
	const content = modules[path];

	if (!content) {
		throw error(404, `Content not found: ${filename}`);
	}
	const nav = getNavigation(slug);

	return {
		content,
		metadata: {},
		slug,
		entry,
		...(nav ?? {})
	};
}
