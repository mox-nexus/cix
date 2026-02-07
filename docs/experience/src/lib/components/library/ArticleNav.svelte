<script lang="ts">
	import type { Quadrant, LibraryEntry } from '$lib/data/library';
	import { base } from '$app/paths';

	interface Props {
		quadrant: Quadrant;
		position: number;
		total: number;
		prev?: LibraryEntry;
		next?: LibraryEntry;
	}

	let { quadrant, position, total, prev, next }: Props = $props();
</script>

<nav class="article-nav" aria-label="Article navigation">
	<span class="article-position">{String(position).padStart(2, '0')} of {String(total).padStart(2, '0')}</span>

	<div class="article-nav-links">
		{#if prev}
			<a href="{base}/library/{quadrant}/{prev.slug}" class="nav-prev">
				<span class="nav-arrow">&larr;</span>
				<span class="nav-label">{prev.title}</span>
			</a>
		{:else}
			<span></span>
		{/if}

		{#if next}
			<a href="{base}/library/{quadrant}/{next.slug}" class="nav-next">
				<span class="nav-label">{next.title}</span>
				<span class="nav-arrow">&rarr;</span>
			</a>
		{:else}
			<a href="{base}/library" class="nav-next">
				<span class="nav-label">Back to Library</span>
				<span class="nav-arrow">&rarr;</span>
			</a>
		{/if}
	</div>
</nav>

<style>
	.article-nav {
		max-width: var(--content-width);
		margin-top: var(--space-4);
		padding-top: var(--space-3);
		border-top: 1px solid var(--dao-border);
	}

	.article-position {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
		display: block;
		margin-bottom: var(--space-2);
	}

	.article-nav-links {
		display: flex;
		justify-content: space-between;
		gap: var(--space-2);
	}

	.nav-prev,
	.nav-next {
		display: inline-flex;
		align-items: baseline;
		gap: 0.5ch;
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-text-secondary);
		text-decoration: none;
		transition: color var(--duration-fast) var(--easing-linear);
	}

	.nav-prev:hover,
	.nav-next:hover {
		color: var(--spark-core);
	}

	.nav-next {
		margin-left: auto;
	}

	.nav-arrow {
		color: var(--dao-muted);
	}

	.nav-prev:hover .nav-arrow,
	.nav-next:hover .nav-arrow {
		color: var(--spark-core);
	}

	@media (prefers-reduced-motion: reduce) {
		.nav-prev,
		.nav-next {
			transition: none;
		}
	}
</style>
