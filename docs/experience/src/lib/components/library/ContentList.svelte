<script lang="ts">
	import type { Quadrant, LibraryEntry } from '$lib/data/library';
	import { base } from '$app/paths';

	interface Props {
		quadrant: Quadrant;
		entries: LibraryEntry[];
		ordered?: boolean;
	}

	let { quadrant, entries, ordered = false }: Props = $props();
</script>

<nav class="content-list" aria-label="{quadrant} articles">
	{#each entries as entry, i}
		<a href="{base}/library/{quadrant}/{entry.slug}" class="list-entry">
			{#if ordered}
				<span class="entry-number">{String(i + 1).padStart(2, '0')}</span>
			{/if}
			<div class="entry-content">
				<span class="entry-title">{entry.title}</span>
				<span class="entry-description">{entry.description}</span>
			</div>
		</a>
		{#if ordered && i < entries.length - 1}
			<div class="entry-connector" aria-hidden="true"></div>
		{/if}
	{/each}
</nav>

<style>
	.content-list {
		display: flex;
		flex-direction: column;
		max-width: 72ch;
		margin: 0 auto;
	}

	.list-entry {
		display: flex;
		align-items: flex-start;
		gap: var(--space-2);
		padding: var(--space-2) var(--space-1);
		text-decoration: none;
		border-radius: var(--radius-sm);
		transition: background var(--duration-fast) var(--easing-linear);
	}

	.list-entry:hover {
		background: var(--dao-surface);
	}

	.entry-number {
		font-family: var(--font-mono);
		font-size: var(--type-lg);
		font-weight: 700;
		color: var(--spark-core);
		min-width: 2.5ch;
		line-height: 1.2;
	}

	.entry-content {
		display: flex;
		flex-direction: column;
		gap: 2px;
	}

	.entry-title {
		font-family: var(--font-sans);
		font-size: var(--type-base);
		font-weight: 600;
		color: var(--dao-text);
	}

	.entry-description {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		line-height: var(--leading-relaxed);
	}

	.entry-connector {
		width: 2px;
		height: var(--space-2);
		background: var(--dao-border);
		margin-left: calc(1.25ch + var(--space-1));
	}

	.list-entry:hover + .entry-connector,
	.entry-connector:has(+ .list-entry:hover) {
		background: var(--spark-core);
		opacity: 0.4;
	}

	@media (prefers-reduced-motion: reduce) {
		.list-entry {
			transition: none;
		}
	}
</style>
