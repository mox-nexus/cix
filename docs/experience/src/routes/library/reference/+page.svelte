<script lang="ts">
	import { LIBRARY } from '$lib/data/library';
	import { base } from '$app/paths';

	let referenceData = $derived(LIBRARY.find((q) => q.id === 'reference'));
</script>

<svelte:head>
	<title>Reference — cix Library</title>
</svelte:head>

<div class="quadrant-index">
	<nav class="quadrant-breadcrumb">
		<a href="{base}/library">library</a>
		<span class="breadcrumb-sep">/</span>
		<span>reference</span>
	</nav>

	<header class="quadrant-header">
		<h1>Reference</h1>
		<p class="tagline">Evidence syntheses and citations.</p>
	</header>

	{#if referenceData}
		<nav class="ref-grid" aria-label="Reference articles">
			{#each referenceData.entries as entry}
				<a href="{base}/library/reference/{entry.slug}" class="ref-link">
					<span class="ref-title">{entry.title}</span>
					<span class="ref-description">{entry.description}</span>
				</a>
			{/each}
		</nav>
	{/if}
</div>

<style>
	.quadrant-index {
		max-width: 72ch;
		margin: 0 auto;
	}

	.quadrant-breadcrumb {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		margin-bottom: var(--space-3);
		display: flex;
		align-items: center;
		gap: 0.5ch;
	}

	.quadrant-breadcrumb a {
		color: var(--dao-muted);
		text-decoration: none;
		transition: color var(--duration-fast) var(--easing-linear);
	}

	.quadrant-breadcrumb a:hover {
		color: var(--spark-core);
	}

	.breadcrumb-sep {
		opacity: 0.6;
	}

	.quadrant-header {
		margin-bottom: var(--space-4);
	}

	.quadrant-header h1 {
		font-size: var(--type-2xl);
		color: var(--quadrant-reference);
		margin: 0 0 var(--space-1) 0;
	}

	.tagline {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		margin: 0;
	}

	.ref-grid {
		display: flex;
		flex-direction: column;
		gap: var(--space-2);
	}

	.ref-link {
		display: block;
		padding: var(--space-2) var(--space-3);
		background: var(--dao-surface);
		border: 1px solid var(--dao-border);
		border-left: 3px solid var(--quadrant-reference);
		border-radius: var(--radius-sm);
		text-decoration: none;
		transition: border-color var(--duration-fast) var(--easing-linear);
	}

	.ref-link:hover {
		border-color: var(--quadrant-reference);
	}

	.ref-title {
		display: block;
		font-family: var(--font-sans);
		font-size: var(--type-base);
		font-weight: 600;
		color: var(--dao-text);
		margin-bottom: 2px;
	}

	.ref-description {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
	}

	@media (prefers-reduced-motion: reduce) {
		.ref-link {
			transition: none;
		}
	}
</style>
