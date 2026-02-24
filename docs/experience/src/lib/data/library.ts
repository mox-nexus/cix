export type Quadrant = 'tutorials' | 'how-to' | 'explanation' | 'reference';
export type Cluster = 'argument' | 'design' | 'limits';
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
		id: 'argument',
		label: 'The Argument',
		description: 'The paradox, its mechanism, and what is at stake',
		order: ['the-paradox', 'the-mechanism', 'the-stakes']
	},
	{
		id: 'design',
		label: 'The Design Response',
		description: 'What the evidence says about design levers and how cix applies them',
		order: ['the-design-lever', 'what-cix-does']
	},
	{
		id: 'limits',
		label: 'Honest Limits',
		description: 'Where the argument is strong, where assembled, where ahead of evidence',
		order: ['honest-limits']
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
				slug: 'the-paradox',
				title: 'The Paradox',
				description:
					'AI reliably improves immediate task performance while simultaneously degrading the cognitive foundations that enable long-term capability.',
				cluster: 'argument',
				difficulty: 'foundational',
				readMinutes: 8,
				related: ['the-mechanism', 'the-stakes']
			},
			{
				slug: 'the-mechanism',
				title: 'The Mechanism',
				description:
					'The generative step — the cognitive work of constructing understanding — is what AI bypasses, and it is where learning happens.',
				cluster: 'argument',
				difficulty: 'intermediate',
				readMinutes: 10,
				prerequisites: ['the-paradox'],
				related: ['the-design-lever', 'honest-limits']
			},
			{
				slug: 'the-design-lever',
				title: 'The Design Lever',
				description:
					'Same tool, different engagement model, opposite outcome: process control and mastery orientation are the measured levers.',
				cluster: 'design',
				difficulty: 'intermediate',
				readMinutes: 10,
				prerequisites: ['the-mechanism'],
				related: ['what-cix-does', 'honest-limits']
			},
			{
				slug: 'the-stakes',
				title: 'The Stakes',
				description:
					'Substitutive AI use produces measurably less diverse output at the individual level and risks model collapse at the systemic level.',
				cluster: 'argument',
				difficulty: 'advanced',
				readMinutes: 10,
				prerequisites: ['the-paradox'],
				related: ['the-design-lever', 'honest-limits']
			},
			{
				slug: 'what-cix-does',
				title: 'What cix Does',
				description:
					'How cix operationalizes the design levers — process control at install, transparency through dual content, mastery through orthogonality.',
				file: 'what-cix-does.md',
				cluster: 'design',
				difficulty: 'intermediate',
				readMinutes: 8,
				prerequisites: ['the-design-lever'],
				related: ['honest-limits', 'the-stakes']
			},
			{
				slug: 'honest-limits',
				title: 'Honest Limits',
				description:
					'What the research has not measured, what claims are assembled rather than demonstrated, and where cix itself remains a bet.',
				file: 'honest-limits.md',
				cluster: 'limits',
				difficulty: 'foundational',
				readMinutes: 8,
				related: ['the-paradox', 'the-mechanism']
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
