export type Quadrant = 'tutorials' | 'how-to' | 'explanation' | 'reference';

export interface LibraryEntry {
	slug: string;
	title: string;
	description: string;
	/** Filename on disk if different from slug */
	file?: string;
}

export interface QuadrantMeta {
	id: Quadrant;
	label: string;
	tagline: string;
	variant: 'spark' | 'emergence' | 'constraint' | 'muted';
	entries: LibraryEntry[];
}

export const LIBRARY: QuadrantMeta[] = [
	{
		id: 'explanation',
		label: 'Explanation',
		tagline: 'The research and reasoning',
		variant: 'spark',
		entries: [
			{
				slug: 'the-problem',
				title: 'The Problem',
				description: 'AI improves task performance while degrading capability.'
			},
			{
				slug: 'the-evidence',
				title: 'The Evidence',
				description: 'Research synthesis from CHI, PNAS, and premier venues.'
			},
			{
				slug: 'why-it-matters',
				title: 'Why It Matters',
				description: 'Stakes of getting collaborative intelligence right.'
			},
			{
				slug: 'skill-formation',
				title: 'Skill Formation',
				description: 'How expertise develops and what threatens it.'
			},
			{
				slug: 'first-principles',
				title: 'First Principles',
				description: 'Core design principles for complementary AI.',
				file: 'first-principles-ci'
			}
		]
	},
	{
		id: 'reference',
		label: 'Reference',
		tagline: 'Facts, specs, and citations',
		variant: 'muted',
		entries: [
			{
				slug: 'bibliography',
				title: 'Bibliography',
				description: 'Full citation list for all research referenced.'
			}
		]
	}
];

export function getQuadrant(id: Quadrant): QuadrantMeta {
	const q = LIBRARY.find((q) => q.id === id);
	if (!q) throw new Error(`Unknown quadrant: ${id}`);
	return q;
}

export function getEntry(quadrant: Quadrant, slug: string): LibraryEntry | undefined {
	return getQuadrant(quadrant).entries.find((e) => e.slug === slug);
}

export function getNavigation(quadrant: Quadrant, slug: string) {
	const q = getQuadrant(quadrant);
	const entries = q.entries;
	const index = entries.findIndex((e) => e.slug === slug);
	if (index === -1) return null;
	return {
		position: index + 1,
		total: entries.length,
		prev: index > 0 ? entries[index - 1] : undefined,
		next: index < entries.length - 1 ? entries[index + 1] : undefined
	};
}
