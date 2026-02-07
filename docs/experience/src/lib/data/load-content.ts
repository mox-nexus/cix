import { error } from '@sveltejs/kit';
import type { Quadrant } from './library';
import { getEntry, getNavigation } from './library';

/**
 * Load markdown content for a library article.
 *
 * Uses Vite's import.meta.glob so the bundler can resolve all content
 * at build time. The quadrant/filename are selected at runtime.
 */
export async function loadLibraryContent(quadrant: Quadrant, slug: string) {
	const entry = getEntry(quadrant, slug);
	if (!entry) {
		throw error(404, `Not found: ${quadrant}/${slug}`);
	}

	const filename = entry.file ?? slug;
	const modules = import.meta.glob('../../../../content/library/**/*.md');
	const path = `../../../../content/library/${quadrant}/${filename}.md`;
	const loader = modules[path];

	if (!loader) {
		throw error(404, `Content not found: ${quadrant}/${filename}`);
	}

	const post = (await loader()) as { default: any; metadata?: Record<string, unknown> };
	const nav = getNavigation(quadrant, slug);

	return {
		content: post.default,
		metadata: post.metadata ?? {},
		quadrant,
		...(nav ?? {})
	};
}
