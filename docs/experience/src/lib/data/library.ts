export type Quadrant = 'tutorials' | 'how-to' | 'explanation' | 'reference';
export type Cluster = 'thesis' | 'mechanisms' | 'ci-systems-design' | 'stakes' | 'synthesis' | 'practice';
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
		description: 'What CI is, why it matters, how to read the evidence critically',
		order: ['what-is-ci', 'first-principles-ci', 'why-it-matters', 'hype-questioning']
	},
	{
		id: 'mechanisms',
		label: 'Mechanisms',
		description: 'How cognitive offloading, skill atrophy, and homogenization work',
		order: ['the-problem', 'cognitive-effects', 'skill-formation', 'diversity-conformity']
	},
	{
		id: 'stakes',
		label: 'Stakes',
		description: 'What is at risk',
		order: ['productivity', 'the-risks']
	},
	{
		id: 'synthesis',
		label: 'Synthesis',
		description: 'Why the evidence is credible — five independent groups, same finding',
		order: ['the-evidence']
	},
	{
		id: 'ci-systems-design',
		label: 'CI Systems Design',
		description: 'The structural levers for complementary AI',
		order: ['collaboration-design']
	},
	{
		id: 'practice',
		label: 'Practice',
		description: 'What the protective pattern looks like in your hands',
		order: ['the-capability-trap', 'the-four-minute-difference']
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
				related: ['first-principles-ci', 'the-capability-trap']
			},
			{
				slug: 'first-principles-ci',
				title: 'First Principles',
				description: 'Core design principles for complementary AI.',
				cluster: 'thesis',
				difficulty: 'intermediate',
				readMinutes: 3,
				prerequisites: ['what-is-ci'],
				related: ['collaboration-design', 'why-it-matters']
			},
			{
				slug: 'why-it-matters',
				title: 'Why It Matters',
				description: 'Stakes of getting collaborative intelligence right.',
				cluster: 'thesis',
				difficulty: 'foundational',
				readMinutes: 4,
				related: ['the-risks', 'the-capability-trap']
			},
			{
				slug: 'hype-questioning',
				title: 'Hype & Questioning',
				description: 'Why critical evaluation of AI claims matters.',
				cluster: 'thesis',
				difficulty: 'foundational',
				readMinutes: 5,
				related: ['productivity', 'the-evidence']
			},
			{
				slug: 'the-problem',
				title: 'The Problem',
				description: 'AI improves task performance while degrading capability.',
				cluster: 'mechanisms',
				difficulty: 'foundational',
				readMinutes: 5,
				related: ['the-evidence', 'the-risks']
			},
			{
				slug: 'cognitive-effects',
				title: 'Cognitive Effects',
				description: 'How AI reshapes thinking and metacognition.',
				cluster: 'mechanisms',
				difficulty: 'advanced',
				readMinutes: 5,
				prerequisites: ['the-problem'],
				related: ['skill-formation', 'the-risks']
			},
			{
				slug: 'skill-formation',
				title: 'Skill Formation',
				description: 'How expertise develops and what threatens it.',
				cluster: 'mechanisms',
				difficulty: 'advanced',
				readMinutes: 5,
				prerequisites: ['the-evidence'],
				related: ['cognitive-effects', 'the-risks']
			},
			{
				slug: 'diversity-conformity',
				title: 'Diversity & Conformity',
				description: 'The homogenization problem and why diversity matters.',
				cluster: 'mechanisms',
				difficulty: 'advanced',
				readMinutes: 5,
				prerequisites: ['cognitive-effects'],
				related: ['cognitive-effects', 'the-risks']
			},
			{
				slug: 'productivity',
				title: 'Productivity',
				description: 'The productivity paradox in AI-assisted development.',
				cluster: 'stakes',
				difficulty: 'intermediate',
				readMinutes: 5,
				related: ['hype-questioning', 'the-evidence']
			},
			{
				slug: 'the-risks',
				title: 'The Risks',
				description: 'What goes wrong when AI substitutes for thinking.',
				cluster: 'stakes',
				difficulty: 'intermediate',
				readMinutes: 5,
				prerequisites: ['what-is-ci'],
				related: ['cognitive-effects', 'skill-formation']
			},
			{
				slug: 'the-evidence',
				title: 'Independent Convergence',
				description: 'Why five independent research groups finding the same pattern matters.',
				cluster: 'synthesis',
				difficulty: 'intermediate',
				readMinutes: 5,
				prerequisites: ['the-problem'],
				related: ['cognitive-effects', 'skill-formation']
			},
			{
				slug: 'collaboration-design',
				title: 'Collaboration Design',
				description: 'What makes human-AI collaboration work.',
				cluster: 'ci-systems-design',
				difficulty: 'intermediate',
				readMinutes: 5,
				prerequisites: ['what-is-ci', 'the-evidence'],
				related: ['first-principles-ci', 'the-four-minute-difference']
			},
			{
				slug: 'the-capability-trap',
				title: 'When the Tool Goes Down',
				description: 'How AI use quietly erodes the capability it appears to replace.',
				cluster: 'practice',
				difficulty: 'foundational',
				readMinutes: 3,
				related: ['the-four-minute-difference', 'skill-formation', 'the-problem']
			},
			{
				slug: 'the-four-minute-difference',
				title: 'The Four-Minute Difference',
				description: 'The interaction pattern that preserves capability instead of replacing it.',
				cluster: 'practice',
				difficulty: 'foundational',
				readMinutes: 4,
				prerequisites: ['the-capability-trap'],
				related: ['skill-formation', 'collaboration-design']
			}
		]
	},
	{
		id: 'how-to',
		label: 'How-To',
		tagline: 'Practices for the working developer',
		variant: 'emergence',
		entries: [
			{
				slug: 'the-path-forward',
				title: 'How to Structure AI Interactions',
				description: 'Evidence-based practices that preserve capability while leveraging AI.',
				difficulty: 'intermediate',
				readMinutes: 8,
				prerequisites: ['what-is-ci'],
				related: ['the-four-minute-difference', 'collaboration-design']
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
