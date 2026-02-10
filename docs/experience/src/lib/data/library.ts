export type Quadrant = 'tutorials' | 'how-to' | 'explanation' | 'reference';
export type Cluster = 'thesis' | 'evidence' | 'design' | 'critique';
export type Difficulty = 'foundational' | 'intermediate' | 'advanced';

export interface LibraryEntry {
	slug: string;
	title: string;
	description: string;
	/** Filename on disk if different from slug */
	file?: string;
	/** Topic cluster for guided navigation */
	cluster?: Cluster;
	/** Reading difficulty */
	difficulty?: Difficulty;
	/** Estimated read time in minutes */
	readMinutes?: number;
	/** Slugs of prerequisite articles */
	prerequisites?: string[];
	/** Slugs of related articles */
	related?: string[];
}

export interface ClusterMeta {
	id: Cluster;
	label: string;
	description: string;
	/** Suggested reading order within cluster */
	order: string[];
}

export interface QuadrantMeta {
	id: Quadrant;
	label: string;
	tagline: string;
	variant: 'spark' | 'emergence' | 'constraint' | 'muted';
	entries: LibraryEntry[];
}

export const CLUSTERS: ClusterMeta[] = [
	{
		id: 'thesis',
		label: 'Thesis',
		description: 'The collaborative intelligence framework',
		order: ['what-is-ci', 'first-principles-ci', 'the-path-forward']
	},
	{
		id: 'evidence',
		label: 'Evidence',
		description: 'Research findings and data',
		order: ['the-problem', 'the-evidence', 'cognitive-effects', 'skill-formation']
	},
	{
		id: 'design',
		label: 'Design',
		description: 'Applied design principles',
		order: ['collaboration-design', 'diversity-conformity']
	},
	{
		id: 'critique',
		label: 'Critique',
		description: 'Critical evaluation and stakes',
		order: ['productivity', 'hype-questioning', 'why-it-matters', 'the-risks']
	}
];

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
				description: 'The collaborative intelligence thesis.',
				cluster: 'thesis',
				difficulty: 'foundational',
				readMinutes: 5,
				related: ['first-principles-ci', 'the-path-forward']
			},
			{
				slug: 'the-risks',
				title: 'The Risks',
				description: 'What goes wrong when AI substitutes for thinking.',
				cluster: 'critique',
				difficulty: 'intermediate',
				readMinutes: 5,
				prerequisites: ['what-is-ci'],
				related: ['cognitive-effects', 'skill-formation']
			},
			{
				slug: 'the-path-forward',
				title: 'The Path Forward',
				description: 'Evidence-based approaches that preserve capability.',
				cluster: 'thesis',
				difficulty: 'intermediate',
				readMinutes: 5,
				prerequisites: ['what-is-ci'],
				related: ['collaboration-design', 'first-principles-ci']
			},
			{
				slug: 'the-problem',
				title: 'The Problem',
				description: 'AI improves task performance while degrading capability.',
				cluster: 'evidence',
				difficulty: 'foundational',
				readMinutes: 5,
				related: ['the-evidence', 'the-risks']
			},
			{
				slug: 'the-evidence',
				title: 'The Evidence',
				description: 'Research synthesis from CHI, PNAS, and premier venues.',
				cluster: 'evidence',
				difficulty: 'intermediate',
				readMinutes: 5,
				prerequisites: ['the-problem'],
				related: ['cognitive-effects', 'skill-formation']
			},
			{
				slug: 'why-it-matters',
				title: 'Why It Matters',
				description: 'Stakes of getting collaborative intelligence right.',
				cluster: 'critique',
				difficulty: 'foundational',
				readMinutes: 4,
				related: ['the-risks', 'the-path-forward']
			},
			{
				slug: 'skill-formation',
				title: 'Skill Formation',
				description: 'How expertise develops and what threatens it.',
				cluster: 'evidence',
				difficulty: 'advanced',
				readMinutes: 5,
				prerequisites: ['the-evidence'],
				related: ['cognitive-effects', 'the-risks']
			},
			{
				slug: 'first-principles-ci',
				title: 'First Principles',
				description: 'Core design principles for complementary AI.',
				cluster: 'thesis',
				difficulty: 'intermediate',
				readMinutes: 3,
				prerequisites: ['what-is-ci'],
				related: ['collaboration-design', 'the-path-forward']
			},
			{
				slug: 'cognitive-effects',
				title: 'Cognitive Effects',
				description: 'How AI reshapes thinking and metacognition.',
				cluster: 'evidence',
				difficulty: 'advanced',
				readMinutes: 5,
				prerequisites: ['the-problem'],
				related: ['skill-formation', 'the-risks']
			},
			{
				slug: 'collaboration-design',
				title: 'Collaboration Design',
				description: 'What makes human-AI collaboration work.',
				cluster: 'design',
				difficulty: 'intermediate',
				readMinutes: 5,
				prerequisites: ['what-is-ci', 'the-evidence'],
				related: ['diversity-conformity', 'first-principles-ci']
			},
			{
				slug: 'diversity-conformity',
				title: 'Diversity & Conformity',
				description: 'The homogenization problem and why diversity matters.',
				cluster: 'design',
				difficulty: 'advanced',
				readMinutes: 5,
				prerequisites: ['collaboration-design'],
				related: ['cognitive-effects', 'the-risks']
			},
			{
				slug: 'productivity',
				title: 'Productivity',
				description: 'The productivity paradox in AI-assisted development.',
				cluster: 'critique',
				difficulty: 'intermediate',
				readMinutes: 5,
				related: ['hype-questioning', 'the-evidence']
			},
			{
				slug: 'hype-questioning',
				title: 'Hype & Questioning',
				description: 'Why critical evaluation of AI claims matters.',
				cluster: 'critique',
				difficulty: 'foundational',
				readMinutes: 5,
				related: ['productivity', 'the-evidence']
			}
		]
	},
	{
		id: 'reference',
		label: 'Reference',
		tagline: 'Evidence syntheses and citations',
		variant: 'muted',
		entries: [
			{
				slug: 'cognitive-effects-evidence',
				title: 'Cognitive Effects Evidence',
				description: 'Research on how AI changes thinking, attention, and metacognition.'
			},
			{
				slug: 'skill-formation-evidence',
				title: 'Skill Formation Evidence',
				description: 'Research on learning, mastery development, and skill atrophy with AI.'
			},
			{
				slug: 'productivity-evidence',
				title: 'Productivity Evidence',
				description: 'Research on AI-assisted productivity, code quality, and security.'
			},
			{
				slug: 'collaboration-design-evidence',
				title: 'Collaboration Design Evidence',
				description: 'Research on what makes human-AI collaboration effective.'
			},
			{
				slug: 'homogenization-evidence',
				title: 'Homogenization Evidence',
				description: 'Research on AI-driven convergence, conformity, and diversity loss.'
			},
			{
				slug: 'bibliography',
				title: 'Bibliography',
				description: 'Full citation list for all research referenced.'
			}
		]
	}
];

// --- Quadrant helpers ---

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

// --- Cluster helpers ---

export function getCluster(id: Cluster): ClusterMeta {
	const c = CLUSTERS.find((c) => c.id === id);
	if (!c) throw new Error(`Unknown cluster: ${id}`);
	return c;
}

export function getClusterEntries(clusterId: Cluster): LibraryEntry[] {
	const cluster = getCluster(clusterId);
	const allEntries = LIBRARY.flatMap((q) => q.entries);
	// Return entries in cluster's defined order
	return cluster.order
		.map((slug) => allEntries.find((e) => e.slug === slug))
		.filter((e): e is LibraryEntry => e !== undefined);
}

/** Get all entries across all quadrants */
export function getAllEntries(): LibraryEntry[] {
	return LIBRARY.flatMap((q) => q.entries);
}

/** Resolve slugs to entries */
export function resolveEntries(slugs: string[]): LibraryEntry[] {
	const all = getAllEntries();
	return slugs
		.map((slug) => all.find((e) => e.slug === slug))
		.filter((e): e is LibraryEntry => e !== undefined);
}
