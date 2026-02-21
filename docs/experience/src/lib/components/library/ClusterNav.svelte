<script lang="ts">
	import type { Cluster, LibraryEntry } from '$lib/data/library';
	import { getCluster } from '$lib/data/library';
	import { readingProgress } from '$lib/stores/reading-progress';
	import { base } from '$app/paths';

	interface Props {
		cluster: Cluster;
		currentSlug: string;
		entries: LibraryEntry[];
		quadrant?: string;
	}

	let { cluster, currentSlug, entries, quadrant = 'explanation' }: Props = $props();
	let clusterMeta = $derived(getCluster(cluster));
</script>

<nav class="cluster-nav" aria-label="Cluster navigation">
	<h4 class="cluster-title">{clusterMeta.label}</h4>
	<ol class="cluster-list">
		{#each entries as entry, i}
			{@const state = $readingProgress.entries[entry.slug] || 'unvisited'}
			<li class:current={entry.slug === currentSlug}>
				{#if entry.slug === currentSlug}
					<span class="cluster-entry current-entry">
						<span class="entry-indicator" class:visited={state === 'visited'} class:completed={state === 'completed'}>
							{#if state === 'completed'}&#10003;{:else}{i + 1}{/if}
						</span>
						<span class="entry-title">{entry.title}</span>
					</span>
				{:else}
					<a href="{base}/library/{quadrant}/{entry.slug}" class="cluster-entry">
						<span class="entry-indicator" class:visited={state === 'visited'} class:completed={state === 'completed'}>
							{#if state === 'completed'}&#10003;{:else}{i + 1}{/if}
						</span>
						<span class="entry-title">{entry.title}</span>
					</a>
				{/if}
			</li>
		{/each}
	</ol>
</nav>

<style>
	.cluster-nav {
		margin-top: var(--space-3);
		padding-top: var(--space-3);
		border-top: 1px solid var(--dao-border-subtle);
	}

	.cluster-title {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
		text-transform: uppercase;
		letter-spacing: var(--tracking-wide);
		margin: 0 0 var(--space-1-5);
	}

	.cluster-list {
		list-style: none;
		padding: 0;
		margin: 0;
		counter-reset: cluster;
	}

	.cluster-entry {
		display: flex;
		align-items: baseline;
		gap: 0.75ch;
		padding: 3px 0;
		font-size: var(--type-xs);
		color: var(--dao-muted);
		text-decoration: none;
		transition: color var(--duration-fast) var(--easing-linear);
	}

	a.cluster-entry:hover {
		color: var(--dao-text);
	}

	.current-entry {
		color: var(--dao-text);
	}

	.entry-indicator {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		width: 1.4em;
		text-align: center;
		flex-shrink: 0;
		color: var(--dao-muted);
	}

	.entry-indicator.visited {
		color: var(--dao-text-secondary);
	}

	.entry-indicator.completed {
		color: var(--emergence-core);
		opacity: 1;
	}

	.entry-title {
		line-height: 1.3;
	}

	li.current .entry-title {
		font-weight: var(--weight-medium);
	}

	@media (prefers-reduced-motion: reduce) {
		.cluster-entry {
			transition: none;
		}
	}
</style>
