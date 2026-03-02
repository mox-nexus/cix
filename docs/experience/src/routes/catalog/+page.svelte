<script lang="ts">
	import type { PageData } from './$types';
	import type { LifecyclePhase, CatalogExtension } from '$lib/types/catalog';
	import { CatalogEntry } from '$lib/components/catalog';
	import { CrossLinks } from '$lib/components/nav';

	let { data }: { data: PageData } = $props();

	let query = $state('');

	const PHASE_ORDER: LifecyclePhase[] = [
		'research',
		'understand',
		'design',
		'craft',
		'measure',
		'foundation',
		'tools'
	];

	const PHASE_LABELS: Record<LifecyclePhase, string> = {
		research: 'Research',
		understand: 'Understand',
		design: 'Design',
		craft: 'Craft',
		measure: 'Measure',
		foundation: 'Foundation',
		tools: 'Tools'
	};

	const PHASE_DESCRIPTIONS: Record<LifecyclePhase, string> = {
		research: 'Literature review, evidence synthesis, citation-grounded knowledge.',
		understand: 'Explanation, documentation, content that lands.',
		design: 'Architecture deliberation, multi-perspective review.',
		craft: 'Build extensions, tools, and the systems behind them.',
		measure: 'Evaluation methodology — write evals that measure what matters.',
		foundation: 'Cross-cutting scaffolds for collaboration and security.',
		tools: 'Infrastructure for the ecosystem.'
	};

	let filtered = $derived(() => {
		const q = query.toLowerCase().trim();
		if (!q) return data.extensions;
		return data.extensions.filter(
			(ext) =>
				ext.slug.includes(q) ||
				ext.tagline.toLowerCase().includes(q) ||
				ext.manifest.description.toLowerCase().includes(q) ||
				ext.kind.includes(q) ||
				ext.tags.some((t) => t.toLowerCase().includes(q))
		);
	});

	let grouped = $derived(() => {
		const exts = filtered();
		const groups: { phase: LifecyclePhase; extensions: CatalogExtension[] }[] = [];
		for (const phase of PHASE_ORDER) {
			const matching = exts.filter((ext) => ext.phase === phase);
			if (matching.length > 0) {
				groups.push({ phase, extensions: matching });
			}
		}
		return groups;
	});
</script>

<svelte:head>
	<title>Catalog — cix</title>
	<meta
		name="description"
		content="Cognitive extensions for collaborative intelligence."
	/>
</svelte:head>

<main id="main" class="catalog-page">
	<header class="catalog-header">
		<h1>Extensions</h1>
		<p class="intro">
			Cognitive extensions grounded in research, designed to amplify
			collaboration.
		</p>
	</header>

	<div class="catalog-search">
		<input
			type="text"
			bind:value={query}
			placeholder="search extensions..."
			class="search-input"
			aria-label="Search extensions"
		/>
	</div>

	<div class="catalog-groups">
		{#each grouped() as group, gi}
			<section class="phase-group">
				<header class="phase-header">
					<h2 class="phase-label">{PHASE_LABELS[group.phase]}</h2>
					<p class="phase-description">{PHASE_DESCRIPTIONS[group.phase]}</p>
				</header>
				<div class="phase-entries">
					{#each group.extensions as ext, i (ext.slug)}
						<CatalogEntry extension={ext} delay={(gi * 3 + i) * 60} />
					{/each}
				</div>
			</section>
		{/each}
		{#if filtered().length === 0}
			<p class="no-results">No extensions match "{query}"</p>
		{/if}
	</div>

	<CrossLinks />
</main>

<style>
	.catalog-page {
		min-height: 100vh;
		min-height: 100dvh;
		padding: var(--space-4) var(--space-3);
		padding-bottom: var(--space-4);
	}

	.catalog-header {
		max-width: 72ch;
		margin: 0 auto var(--space-3);
	}

	.catalog-header h1 {
		font-size: var(--type-2xl);
		margin: 0 0 var(--space-1) 0;
	}

	.intro {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		line-height: var(--leading-relaxed);
		margin: 0;
	}

	.catalog-search {
		max-width: 72ch;
		margin: 0 auto var(--space-3);
	}

	.search-input {
		width: 100%;
		padding: var(--space-1) var(--space-2);
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-text);
		background: var(--dao-surface);
		border: 1px solid var(--dao-border);
		outline: none;
		transition: border-color var(--duration-fast) var(--easing-linear);
	}

	.search-input::placeholder {
		color: var(--dao-muted);
	}

	.search-input:focus {
		border-color: var(--spark-core);
	}

	.catalog-groups {
		display: flex;
		flex-direction: column;
		gap: var(--space-4);
		max-width: 72ch;
		margin: 0 auto;
	}

	.phase-group {
		display: flex;
		flex-direction: column;
		gap: var(--space-2);
	}

	.phase-header {
		border-bottom: 1px solid var(--dao-border);
		padding-bottom: var(--space-1);
	}

	.phase-label {
		font-family: var(--font-sans);
		font-size: var(--type-base);
		font-weight: 600;
		color: var(--dao-text);
		margin: 0;
		text-transform: lowercase;
	}

	.phase-description {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
		margin: var(--space-0-5) 0 0 0;
		line-height: var(--leading-relaxed);
	}

	.phase-entries {
		display: flex;
		flex-direction: column;
		gap: var(--space-2);
	}

	.no-results {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		text-align: center;
		padding: var(--space-4) 0;
	}

	@media (prefers-reduced-motion: reduce) {
		.search-input {
			transition: none;
		}
	}
</style>
