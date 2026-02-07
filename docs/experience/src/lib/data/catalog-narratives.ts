export interface CatalogNarrative {
	narrativeHook: string;
	constraint: string;
}

export const CATALOG_NARRATIVES: Record<string, CatalogNarrative> = {
	'arch-guild': {
		narrativeHook: 'Architectural reasoning through multi-perspective council deliberation.',
		constraint: 'Enable Diversity'
	},
	'build-evals': {
		narrativeHook: 'Rigorous evaluation methodology for AI agents, skills, and prompts.',
		constraint: 'Evidence-Driven Design'
	},
	'core-ci': {
		narrativeHook: 'Foundational patterns for collaborative intelligence — decisions, verification, first principles.',
		constraint: 'Require Judgment'
	},
	'data-store': {
		narrativeHook: 'Storage and retrieval patterns — databases, search, embeddings, RAG systems.',
		constraint: 'Transparent by Design'
	},
	'extension-dev': {
		narrativeHook: 'Build extensions that enable effective human-AI collaboration.',
		constraint: 'Enable Diversity'
	}
};
