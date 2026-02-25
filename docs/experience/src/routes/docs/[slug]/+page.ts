import { loadDocsContent } from '$lib/data/load-content';
import type { PageLoad } from './$types';

export const load: PageLoad = ({ params }) => loadDocsContent(params.slug);
