import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { findExtension } from '$lib/data/catalog-server';

export const load: PageServerLoad = async ({ params }) => {
	const extension = findExtension(params.slug);
	if (!extension) throw error(404, `Extension not found: ${params.slug}`);
	return { extension };
};
