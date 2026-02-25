export interface DocsEntry {
	slug: string;
	title: string;
	description: string;
	/** Filename on disk if different from slug */
	file?: string;
	/** Content kind */
	kind: 'explanation' | 'reference';
	/** Estimated read time in minutes */
	readMinutes?: number;
	/** Slugs of prerequisite articles */
	prerequisites?: string[];
	/** Slugs of related articles */
	related?: string[];
}

export interface ReadingPath {
	id: string;
	label: string;
	constituency: string;
	hook: string;
	articles: string[];
}

export const DOCS_ENTRIES: DocsEntry[] = [
	{
		slug: 'the-productivity-trap',
		title: 'The Productivity Trap',
		description:
			'AI reliably improves task performance while degrading the cognitive foundations for long-term capability. The person it happens to cannot tell.',
		kind: 'explanation',
		readMinutes: 10,
		related: ['same-tool-different-design']
	},
	{
		slug: 'same-tool-different-design',
		title: 'Same Tool. Different Design.',
		description:
			'The harm is not a property of AI — it is a property of the default engagement model. Design can produce the gain without the harm.',
		kind: 'explanation',
		readMinutes: 10,
		prerequisites: ['the-productivity-trap'],
		related: ['the-design-choices-behind-cix']
	},
	{
		slug: 'the-design-choices-behind-cix',
		title: 'The Design Choices Behind cix',
		description:
			'How cix operationalizes the design levers, where the evidence ends, and where the bet begins.',
		kind: 'explanation',
		readMinutes: 10,
		prerequisites: ['same-tool-different-design'],
		related: ['the-productivity-trap']
	},
	{
		slug: 'bibliography',
		title: 'Bibliography',
		description: 'Full citation list for all research referenced.',
		kind: 'reference'
	}
];

export const READING_PATHS: ReadingPath[] = [
	{
		id: 'builder',
		label: 'Building with AI',
		constituency: 'Developers and engineers',
		hook: 'Your skills may be degrading and you cannot tell.',
		articles: [
			'the-productivity-trap',
			'same-tool-different-design',
			'the-design-choices-behind-cix'
		]
	},
	{
		id: 'deciding',
		label: 'Evaluating AI adoption',
		constituency: 'Engineering leads and decision makers',
		hook: 'The 26% productivity gain is real. So is the skill degradation.',
		articles: [
			'the-productivity-trap',
			'same-tool-different-design',
			'the-design-choices-behind-cix'
		]
	},
	{
		id: 'designing',
		label: 'Designing AI systems',
		constituency: 'Architects and tool designers',
		hook: 'The engagement model is the design variable.',
		articles: [
			'the-productivity-trap',
			'same-tool-different-design',
			'the-design-choices-behind-cix'
		]
	}
];

// --- Entry helpers ---

/** Get a single entry by slug */
export function getEntry(slug: string): DocsEntry | undefined {
	return DOCS_ENTRIES.find((e) => e.slug === slug);
}

/** Get all entries */
export function getAllEntries(): DocsEntry[] {
	return DOCS_ENTRIES;
}

/** Get explanation entries only (ordered) */
export function getExplanationEntries(): DocsEntry[] {
	return DOCS_ENTRIES.filter((e) => e.kind === 'explanation');
}

/** Get prev/next navigation for an entry */
export function getNavigation(slug: string) {
	const entries = getExplanationEntries();
	const index = entries.findIndex((e) => e.slug === slug);
	if (index === -1) return null;
	return {
		position: index + 1,
		total: entries.length,
		prev: index > 0 ? entries[index - 1] : undefined,
		next: index < entries.length - 1 ? entries[index + 1] : undefined
	};
}

/** Resolve slugs to entries */
export function resolveEntries(slugs: string[]): DocsEntry[] {
	return slugs
		.map((slug) => DOCS_ENTRIES.find((e) => e.slug === slug))
		.filter((e): e is DocsEntry => e !== undefined);
}

/** Get a reading path by id */
export function getReadingPath(id: string): ReadingPath | undefined {
	return READING_PATHS.find((p) => p.id === id);
}

/** Get entries for a reading path */
export function getPathEntries(pathId: string): DocsEntry[] {
	const path = getReadingPath(pathId);
	if (!path) return [];
	return resolveEntries(path.articles);
}

/** Total read time for a reading path in minutes */
export function getPathReadTime(pathId: string): number {
	return getPathEntries(pathId).reduce((sum, e) => sum + (e.readMinutes ?? 0), 0);
}
