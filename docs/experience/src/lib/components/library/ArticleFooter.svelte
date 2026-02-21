<script lang="ts">
	import type { Quadrant, LibraryEntry } from '$lib/data/library';
	import { resolveEntries } from '$lib/data/library';
	import { readingProgress, getReadingState } from '$lib/stores/reading-progress';
	import { base } from '$app/paths';

	interface Props {
		slug: string;
		quadrant: Quadrant;
		entry?: LibraryEntry;
		prev?: LibraryEntry;
		next?: LibraryEntry;
		position?: number;
		total?: number;
	}

	let { slug, quadrant, entry, prev, next, position, total }: Props = $props();

	let state = $derived.by(() => {
		const s = $readingProgress.entries[slug];
		return s || 'unvisited';
	});
	let isCompleted = $derived(state === 'completed');
	let relatedEntries = $derived(entry?.related ? resolveEntries(entry.related) : []);
</script>

<footer class="article-footer">
	<!-- Mark as read -->
	<div class="read-action">
		<button
			class="mark-read-btn"
			class:completed={isCompleted}
			onclick={() => readingProgress.toggleCompleted(slug)}
			aria-pressed={isCompleted}
		>
			{#if isCompleted}
				<span class="check-icon">&#10003;</span> Read
			{:else}
				<span class="circle-icon">&#9675;</span> Mark as read
			{/if}
		</button>
		{#if position && total}
			<span class="position-label">{position} of {total}</span>
		{/if}
	</div>

	<!-- Related articles -->
	{#if relatedEntries.length > 0}
		<div class="related-section">
			<h4 class="related-title">Related</h4>
			<ul class="related-list">
				{#each relatedEntries as related}
					{@const relState = $readingProgress.entries[related.slug] || 'unvisited'}
					<li>
						<a href="{base}/library/{quadrant}/{related.slug}" class="related-link">
							<span class="related-indicator" class:completed={relState === 'completed'}>
								{#if relState === 'completed'}&#10003;{:else if relState === 'visited'}&#9679;{:else}&#9675;{/if}
							</span>
							<span>
								<span class="related-name">{related.title}</span>
								{#if related.readMinutes}
									<span class="related-meta">{related.readMinutes} min</span>
								{/if}
							</span>
						</a>
					</li>
				{/each}
			</ul>
		</div>
	{/if}

	<!-- Sequential navigation -->
	<nav class="seq-nav" aria-label="Article navigation">
		<div class="seq-nav-links">
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
</footer>

<style>
	.article-footer {
		margin-top: var(--space-4);
		padding-top: var(--space-3);
		border-top: 1px solid var(--dao-border);
	}

	/* --- Mark as Read --- */

	.read-action {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: var(--space-3);
	}

	.mark-read-btn {
		display: inline-flex;
		align-items: center;
		gap: 0.5ch;
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		background: transparent;
		border: 1px solid var(--dao-border);
		padding: var(--space-0-5) var(--space-2);
		cursor: pointer;
		border-radius: var(--radius-sm);
		transition:
			color var(--duration-fast) var(--easing-linear),
			border-color var(--duration-fast) var(--easing-linear);
	}

	.mark-read-btn:hover {
		color: var(--dao-text);
		border-color: var(--dao-text-secondary);
	}

	.mark-read-btn.completed {
		color: var(--emergence-core);
		border-color: var(--emergence-core);
	}

	.mark-read-btn.completed:hover {
		opacity: 0.8;
	}

	.check-icon {
		color: var(--emergence-core);
	}

	.circle-icon {
		opacity: 0.7;
	}

	.position-label {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
	}

	/* --- Related --- */

	.related-section {
		margin-bottom: var(--space-3);
	}

	.related-title {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
		text-transform: uppercase;
		letter-spacing: var(--tracking-wide);
		margin: 0 0 var(--space-1);
	}

	.related-list {
		list-style: none;
		padding: 0;
		margin: 0;
	}

	.related-link {
		display: flex;
		align-items: baseline;
		gap: 0.75ch;
		padding: var(--space-0-5) 0;
		font-size: var(--type-sm);
		color: var(--dao-text-secondary);
		text-decoration: none;
		transition: color var(--duration-fast) var(--easing-linear);
	}

	.related-link:hover {
		color: var(--dao-text);
	}

	.related-indicator {
		font-size: 0.625rem;
		color: var(--dao-muted);
		flex-shrink: 0;
	}

	.related-indicator.completed {
		color: var(--emergence-core);
	}

	.related-name {
		font-family: var(--font-sans);
	}

	.related-meta {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
		margin-left: 0.5ch;
	}

	/* --- Sequential Nav --- */

	.seq-nav {
		padding-top: var(--space-2);
		border-top: 1px solid var(--dao-border-subtle);
	}

	.seq-nav-links {
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
		.mark-read-btn,
		.related-link,
		.nav-prev,
		.nav-next {
			transition: none;
		}
	}
</style>
