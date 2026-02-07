<script lang="ts">
	import type { Quadrant, LibraryEntry } from '$lib/data/library';
	import { getQuadrant } from '$lib/data/library';
	import ArticleNav from './ArticleNav.svelte';
	import { GlyphBackground } from '$lib/components/atmosphere';

	interface Props {
		quadrant: Quadrant;
		content: any;
		metadata?: Record<string, unknown>;
		position?: number;
		total?: number;
		prev?: LibraryEntry;
		next?: LibraryEntry;
	}

	let { quadrant, content, metadata, position, total, prev, next }: Props = $props();

	let quadrantMeta = $derived(getQuadrant(quadrant));
	let Content = $derived(content);
</script>

<svelte:head>
	<title>{metadata?.title || 'Article'} — cix Library</title>
</svelte:head>

<GlyphBackground />

<div class="article-wrapper">
	<nav class="article-breadcrumb">
		<a href="/library">library</a>
		<span class="breadcrumb-sep">/</span>
		<a href="/library#{quadrant}">{quadrantMeta.label.toLowerCase()}</a>
	</nav>

	<article class="prose">
		<Content />
	</article>

	{#if position && total}
		<ArticleNav {quadrant} {position} {total} {prev} {next} />
	{:else}
		<nav class="article-back">
			<a href="/library#{quadrant}">&larr; {quadrantMeta.label}</a>
		</nav>
	{/if}
</div>

<style>
	.article-wrapper {
		max-width: var(--content-width);
		margin: 0 auto;
	}

	.article-breadcrumb {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		margin-bottom: var(--space-3);
		display: flex;
		align-items: center;
		gap: 0.5ch;
	}

	.article-breadcrumb a {
		color: var(--dao-muted);
		text-decoration: none;
		transition: color var(--duration-fast) var(--easing-linear);
	}

	.article-breadcrumb a:hover {
		color: var(--spark-core);
	}

	.breadcrumb-sep {
		opacity: 0.4;
	}

	.article-back {
		margin-top: var(--space-4);
		padding-top: var(--space-3);
		border-top: 1px solid var(--dao-border);
	}

	.article-back a {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		text-decoration: none;
		transition: color var(--duration-fast) var(--easing-linear);
	}

	.article-back a:hover {
		color: var(--spark-core);
	}

	.prose :global(h1) {
		font-size: var(--type-xl);
		margin-bottom: var(--space-3);
	}

	.prose :global(h2) {
		font-size: var(--type-lg);
		margin-top: var(--space-4);
		margin-bottom: var(--space-2);
	}

	.prose :global(h3) {
		font-size: var(--type-base);
		font-weight: 600;
		margin-top: var(--space-3);
		margin-bottom: var(--space-1);
	}

	.prose :global(p) {
		margin-bottom: var(--space-2);
	}

	.prose :global(ul),
	.prose :global(ol) {
		margin-bottom: var(--space-2);
		padding-left: var(--space-3);
	}

	.prose :global(li) {
		margin-bottom: var(--space-1);
	}

	.prose :global(blockquote) {
		margin: var(--space-3) 0;
	}

	.prose :global(pre) {
		margin: var(--space-2) 0;
	}

	.prose :global(table) {
		margin: var(--space-3) 0;
	}

	.prose :global(hr) {
		margin: var(--space-4) 0;
	}

	@media (prefers-reduced-motion: reduce) {
		.article-breadcrumb a,
		.article-back a {
			transition: none;
		}
	}
</style>
