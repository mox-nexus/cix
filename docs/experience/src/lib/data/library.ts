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
				slug: 'what-is-ci',
				title: 'What is CI',
				description: 'The collaborative intelligence thesis.'
			},
			{
				slug: 'the-risks',
				title: 'The Risks',
				description: 'What goes wrong when AI substitutes for thinking.'
			},
			{
				slug: 'the-path-forward',
				title: 'The Path Forward',
				description: 'Evidence-based approaches that preserve capability.'
			},
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
				slug: 'first-principles-ci',
				title: 'First Principles',
				description: 'Core design principles for complementary AI.'
			},
			{
				slug: 'cognitive-effects',
				title: 'Cognitive Effects',
				description: 'How AI reshapes thinking and metacognition.'
			},
			{
				slug: 'collaboration-design',
				title: 'Collaboration Design',
				description: 'What makes human-AI collaboration work.'
			},
			{
				slug: 'diversity-conformity',
				title: 'Diversity & Conformity',
				description: 'The homogenization problem and why diversity matters.'
			},
			{
				slug: 'productivity',
				title: 'Productivity',
				description: 'The productivity paradox in AI-assisted development.'
			},
			{
				slug: 'hype-questioning',
				title: 'Hype & Questioning',
				description: 'Why critical evaluation of AI claims matters.'
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
