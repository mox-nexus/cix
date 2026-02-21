<script lang="ts">
	import { LIBRARY, CLUSTERS, getClusterEntries } from '$lib/data/library';
	import type { Cluster } from '$lib/data/library';
	import { readingProgress } from '$lib/stores/reading-progress';
	import { base } from '$app/paths';

	const DIFFICULTY_ICON: Record<string, string> = {
		foundational: '○',
		intermediate: '◐',
		advanced: '●'
	};

	const STATE_ICON: Record<string, string> = {
		unvisited: '○',
		visited: '◐',
		completed: '●'
	};

	let progress = $derived($readingProgress);

	function entryState(slug: string): string {
		return progress.entries[slug] || 'unvisited';
	}

	function clusterProgress(clusterId: Cluster) {
		const entries = getClusterEntries(clusterId);
		const completed = entries.filter((e) => entryState(e.slug) === 'completed').length;
		return { completed, total: entries.length };
	}
</script>

<svelte:head>
	<title>Explanation — cix Library</title>
</svelte:head>

<div class="quadrant-index">
	<nav class="quadrant-breadcrumb">
		<a href="{base}/library">library</a>
		<span class="breadcrumb-sep">/</span>
		<span>explanation</span>
	</nav>

	<header class="quadrant-header">
		<h1>Explanation</h1>
		<p class="tagline">The research and reasoning behind collaborative intelligence.</p>
	</header>

	{#each CLUSTERS as cluster}
		{@const entries = getClusterEntries(cluster.id)}
		{@const cp = clusterProgress(cluster.id)}
		<section class="cluster-group">
			<div class="cluster-header">
				<h2 class="cluster-label">{cluster.label}</h2>
				<span class="cluster-description">{cluster.description}</span>
				<span class="cluster-progress">{cp.completed}/{cp.total}</span>
			</div>

			<nav class="cluster-entries" aria-label="{cluster.label} articles">
				{#each entries as entry, ei}
					{@const state = entryState(entry.slug)}
					<a
						href="{base}/library/explanation/{entry.slug}"
						class="entry"
						class:is-completed={state === 'completed'}
						class:is-visited={state === 'visited'}
					>
						<span class="entry-index">{ei + 1}</span>
						<div class="entry-body">
							<div class="entry-top">
								<span class="entry-title">{entry.title}</span>
								<span class="entry-meta">
									{#if entry.readMinutes}{entry.readMinutes} min{/if}
									{#if entry.difficulty}
										<span class="entry-difficulty" title={entry.difficulty}>
											{DIFFICULTY_ICON[entry.difficulty]}
										</span>
									{/if}
								</span>
							</div>
							<span class="entry-description">{entry.description}</span>
						</div>
						<span class="entry-state" title={state}>
							{STATE_ICON[state]}
						</span>
					</a>
					{#if ei < entries.length - 1}
						<div class="entry-connector" aria-hidden="true"></div>
					{/if}
				{/each}
			</nav>
		</section>
	{/each}
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
		color: var(--quadrant-explanation);
		margin: 0 0 var(--space-1) 0;
	}

	.tagline {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		margin: 0;
	}

	/* --- Cluster Groups --- */

	.cluster-group {
		margin-bottom: var(--space-4);
	}

	.cluster-header {
		margin-bottom: var(--space-1);
		padding-bottom: var(--space-1);
		border-bottom: 1px solid var(--dao-border-subtle);
		display: flex;
		align-items: baseline;
		gap: var(--space-2);
		flex-wrap: wrap;
	}

	.cluster-label {
		font-family: var(--font-sans);
		font-size: var(--type-sm);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		color: var(--dao-text-secondary);
		margin: 0;
		font-weight: 600;
	}

	.cluster-description {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		flex: 1;
	}

	.cluster-progress {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
	}

	/* --- Entries --- */

	.cluster-entries {
		display: flex;
		flex-direction: column;
	}

	.entry {
		display: flex;
		align-items: flex-start;
		gap: var(--space-2);
		padding: var(--space-1-5) var(--space-1);
		text-decoration: none;
		border-radius: var(--radius-sm);
		transition: background var(--duration-fast) var(--easing-linear);
	}

	.entry:hover {
		background: var(--dao-surface);
	}

	.entry-index {
		font-family: var(--font-mono);
		font-size: var(--type-lg);
		font-weight: 700;
		color: var(--dao-muted);
		min-width: 2ch;
		text-align: right;
		line-height: 1.2;
	}

	.entry.is-visited .entry-index {
		color: var(--dao-text-secondary);
	}

	.entry.is-completed .entry-index {
		color: var(--spark-core);
	}

	.entry-body {
		flex: 1;
		min-width: 0;
	}

	.entry-top {
		display: flex;
		align-items: baseline;
		gap: var(--space-2);
		margin-bottom: 2px;
	}

	.entry-title {
		font-family: var(--font-sans);
		font-size: var(--type-base);
		font-weight: 600;
		color: var(--dao-text);
	}

	.entry-meta {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
		display: flex;
		align-items: center;
		gap: 0.5ch;
		white-space: nowrap;
	}

	.entry-difficulty {
		font-size: 0.7em;
	}

	.entry-description {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		line-height: var(--leading-relaxed);
	}

	.entry-state {
		font-size: var(--type-sm);
		color: var(--dao-muted);
		min-width: 1.5ch;
		text-align: center;
		line-height: 1.4;
	}

	.entry.is-visited .entry-state {
		color: var(--dao-text-secondary);
	}

	.entry.is-completed .entry-state {
		color: var(--spark-core);
	}

	.entry-connector {
		width: 2px;
		height: var(--space-1);
		background: var(--dao-border);
		margin-left: calc(1ch + var(--space-1));
	}

	@media (prefers-reduced-motion: reduce) {
		.entry {
			transition: none;
		}
	}
</style>
