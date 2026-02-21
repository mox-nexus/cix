<script lang="ts">
	import { LIBRARY } from '$lib/data/library';
	import { readingProgress } from '$lib/stores/reading-progress';
	import { CrossLinks } from '$lib/components/nav';
	import QuadrantCard from './QuadrantCard.svelte';

	const QUADRANT_ORDER = [
		{ id: 'explanation', label: 'Explanation', tagline: 'The research and reasoning' },
		{ id: 'how-to', label: 'How-To', tagline: 'Practical guides for building extensions' },
		{ id: 'tutorials', label: 'Tutorials', tagline: 'Hands-on learning from first principles' },
		{ id: 'reference', label: 'Reference', tagline: 'Evidence syntheses and citations' }
	];

	const CLUSTER_PREVIEW: Record<string, string> = {
		explanation: 'Thesis \u00B7 Evidence \u00B7 Design \u00B7 Critique'
	};

	let progress = $derived($readingProgress);

	function quadrantCount(id: string): number {
		return LIBRARY.find((q) => q.id === id)?.entries.length ?? 0;
	}

	function quadrantProgress(id: string): { completed: number; total: number } {
		const data = LIBRARY.find((q) => q.id === id);
		if (!data) return { completed: 0, total: 0 };
		const completed = data.entries.filter(
			(e) => progress.entries[e.slug] === 'completed'
		).length;
		return { completed, total: data.entries.length };
	}
</script>

<svelte:head>
	<title>Library — cix</title>
	<meta
		name="description"
		content="Research and practice of collaborative intelligence. Explanation, reference, and guides organized by Diataxis quadrant."
	/>
</svelte:head>

<div class="library-index">
	<header class="library-header">
		<h1>Library</h1>
		<p class="intro">
			The research behind collaborative intelligence — organized by purpose,
			ordered for progressive understanding.
		</p>
	</header>

	<div class="quadrant-grid" role="navigation" aria-label="Content quadrants">
		{#each QUADRANT_ORDER as q, i}
			{@const count = quadrantCount(q.id)}
			{@const isPlaceholder = count === 0}

			<QuadrantCard
				id={q.id}
				label={q.label}
				tagline={q.tagline}
				{count}
				preview={CLUSTER_PREVIEW[q.id]}
				progress={quadrantProgress(q.id)}
				placeholder={isPlaceholder}
				variant={q.id}
				delay={i * 80}
			/>
		{/each}
	</div>

	<CrossLinks />
</div>

<style>
	.library-index {
		max-width: 72ch;
		margin: 0 auto;
	}

	.library-header {
		margin-bottom: var(--space-4);
	}

	.library-header h1 {
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

	.quadrant-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: var(--space-3);
		margin-bottom: var(--space-4);
	}

	@media (max-width: 600px) {
		.quadrant-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
