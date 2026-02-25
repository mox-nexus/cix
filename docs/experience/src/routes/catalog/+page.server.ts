import type { PageServerLoad } from './$types';
import { loadAllExtensions } from '$lib/data/catalog-server';

export const load: PageServerLoad = async () => {
	const extensions = loadAllExtensions();
	return { extensions };
};
