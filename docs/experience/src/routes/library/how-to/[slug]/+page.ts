import { loadLibraryContent } from '$lib/data/load-content';
import type { PageLoad } from './$types';

export const load: PageLoad = ({ params }) => loadLibraryContent('how-to', params.slug);
