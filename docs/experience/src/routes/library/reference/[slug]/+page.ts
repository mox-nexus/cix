import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';

const fileMap: Record<string, string> = {
	'bibliography': 'bibliography'
};

export const load: PageLoad = async ({ params }) => {
	const { slug } = params;
	const filename = fileMap[slug];

	if (!filename) {
		throw error(404, `Page not found: ${slug}`);
	}

	try {
		const post = await import(`../../../../../../content/library/reference/${filename}.md`);

		return {
			content: post.default,
			metadata: post.metadata || {}
		};
	} catch (e) {
		throw error(404, `Could not load: ${slug}`);
	}
};
