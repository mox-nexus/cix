import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';

// Map slugs to actual filenames
const fileMap: Record<string, string> = {
	'the-problem': 'the-problem',
	'the-evidence': 'the-evidence',
	'why-it-matters': 'why-it-matters',
	'skill-formation': 'skill-formation',
	'first-principles': 'first-principles-ci'
};

export const load: PageLoad = async ({ params }) => {
	const { slug } = params;
	const filename = fileMap[slug];

	if (!filename) {
		throw error(404, `Page not found: ${slug}`);
	}

	try {
		// Dynamic import of markdown file
		const post = await import(`../../../../../../content/library/explanation/${filename}.md`);

		return {
			content: post.default,
			metadata: post.metadata || {}
		};
	} catch (e) {
		throw error(404, `Could not load: ${slug}`);
	}
};
