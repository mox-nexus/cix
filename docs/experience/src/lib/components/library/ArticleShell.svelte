<script lang="ts">
	import { onMount } from 'svelte';
	import type { Quadrant, LibraryEntry } from '$lib/data/library';
	import { getQuadrant, getClusterEntries } from '$lib/data/library';
	import { readingProgress } from '$lib/stores/reading-progress';
	import { base } from '$app/paths';
	import TableOfContents from './TableOfContents.svelte';
	import ClusterNav from './ClusterNav.svelte';
	import ArticleFooter from './ArticleFooter.svelte';
	import EvidencePopover from './EvidencePopover.svelte';

	interface Props {
		quadrant: Quadrant;
		slug?: string;
		entry?: LibraryEntry;
		content: any;
		metadata?: Record<string, unknown>;
		position?: number;
		total?: number;
		prev?: LibraryEntry;
		next?: LibraryEntry;
	}

	let { quadrant, slug, entry, content, metadata, position, total, prev, next }: Props = $props();

	let quadrantMeta = $derived(getQuadrant(quadrant));
	let Content = $derived(content);
	let clusterEntries = $derived(
		entry?.cluster ? getClusterEntries(entry.cluster) : []
	);

	// Extract headings + title client-side (markdown has no frontmatter)
	let headings = $state<{ id: string; text: string; level: number }[]>([]);
	let articleTitle = $state(metadata?.title as string || '');
	let articleEl: HTMLElement | undefined = $state();

	// Evidence popover state
	type EvidenceLevel = 'strong' | 'moderate' | 'weak' | 'speculative';
	let evTarget = $state<HTMLElement | null>(null);
	let evLevel = $state<EvidenceLevel>('moderate');
	let evSource = $state('');
	let evVisible = $state(false);

	function extractLevel(el: HTMLElement): EvidenceLevel {
		if (el.classList.contains('ev-strong')) return 'strong';
		if (el.classList.contains('ev-moderate')) return 'moderate';
		if (el.classList.contains('ev-weak')) return 'weak';
		if (el.classList.contains('ev-speculative')) return 'speculative';
		return 'moderate';
	}

	function showPopover(badge: HTMLElement) {
		evTarget = badge;
		evLevel = extractLevel(badge);
		evSource = badge.getAttribute('title') || '';
		evVisible = true;
		// Remove native tooltip while popover is shown
		badge.removeAttribute('title');
		badge.dataset.title = evSource;
	}

	function closePopover() {
		// Restore native title on the badge
		if (evTarget && evTarget.dataset.title) {
			evTarget.setAttribute('title', evTarget.dataset.title);
			delete evTarget.dataset.title;
		}
		evVisible = false;
		evTarget = null;
	}

	onMount(() => {
		if (!articleEl) return;
		// Mark article as visited
		if (slug) readingProgress.markVisited(slug);
		// Extract h1 for page title
		const h1 = articleEl.querySelector('h1');
		if (h1 && !articleTitle) articleTitle = h1.textContent || '';
		// Extract h2/h3 for ToC
		const els = articleEl.querySelectorAll('h2, h3');
		headings = Array.from(els).map((el) => ({
			id: el.id,
			text: el.textContent || '',
			level: parseInt(el.tagName[1])
		}));

		// Upgrade evidence badges with accessibility + click handlers
		const badges = articleEl.querySelectorAll<HTMLElement>('.ev');
		badges.forEach((badge) => {
			badge.setAttribute('tabindex', '0');
			badge.setAttribute('role', 'note');
			const title = badge.getAttribute('title');
			if (title) badge.setAttribute('aria-label', `Evidence: ${title}`);

			badge.addEventListener('click', (e) => {
				e.stopPropagation();
				if (evVisible && evTarget === badge) {
					closePopover();
				} else {
					showPopover(badge);
				}
			});

			badge.addEventListener('keydown', (e) => {
				if (e.key === 'Enter' || e.key === ' ') {
					e.preventDefault();
					if (evVisible && evTarget === badge) {
						closePopover();
					} else {
						showPopover(badge);
					}
				}
			});
		});

		// Click-outside dismissal
		function handleClickOutside(e: MouseEvent) {
			if (!evVisible) return;
			const target = e.target as HTMLElement;
			if (target.closest('.ev') || target.closest('.ev-popover')) return;
			closePopover();
		}

		// Escape key dismissal
		function handleKeydown(e: KeyboardEvent) {
			if (e.key === 'Escape' && evVisible) closePopover();
		}

		document.addEventListener('click', handleClickOutside);
		document.addEventListener('keydown', handleKeydown);

		return () => {
			document.removeEventListener('click', handleClickOutside);
			document.removeEventListener('keydown', handleKeydown);
		};
	});
</script>

<svelte:head>
	<title>{articleTitle || 'Article'} — cix Library</title>
</svelte:head>

<div class="article-layout">
	<article class="library-prose" bind:this={articleEl}>
		<nav class="article-breadcrumb">
			<a href="{base}/library">library</a>
			<span class="breadcrumb-sep">/</span>
			<a href="{base}/library#{quadrant}">{quadrantMeta.label.toLowerCase()}</a>
		</nav>

		<Content />

		{#if slug}
			<ArticleFooter
				{slug}
				{quadrant}
				{entry}
				{prev}
				{next}
				{position}
				{total}
			/>
		{:else}
			<nav class="article-back">
				<a href="{base}/library#{quadrant}">&larr; {quadrantMeta.label}</a>
			</nav>
		{/if}
	</article>

	<aside class="article-sidebar">
		<TableOfContents {headings} />
		{#if entry?.cluster && slug}
			<ClusterNav
				cluster={entry.cluster}
				currentSlug={slug}
				entries={clusterEntries}
				{quadrant}
			/>
		{/if}
	</aside>
</div>

<EvidencePopover
	target={evTarget}
	level={evLevel}
	source={evSource}
	visible={evVisible}
	onclose={closePopover}
/>

<style>
	/* ===========================================
	   ARTICLE LAYOUT: Two-Column Grid
	   Content (65ch) + Sticky Sidebar (ToC)
	   =========================================== */

	.article-layout {
		display: grid;
		grid-template-columns: 1fr var(--toc-width);
		gap: var(--space-4);
		max-width: calc(var(--content-width) + var(--toc-width) + var(--space-4));
		margin: 0 auto;
	}

	.article-sidebar {
		position: sticky;
		top: calc(72px + var(--space-3));
		max-height: calc(100vh - 72px - var(--space-6));
		overflow-y: auto;
	}

	@media (max-width: 900px) {
		.article-layout {
			grid-template-columns: 1fr;
		}

		.article-sidebar {
			display: none;
		}
	}

	/* ===========================================
	   ARTICLE CHROME: Breadcrumb + Back Link
	   Stays monospace — structural navigation
	   =========================================== */

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

	/* ===========================================
	   LIBRARY PROSE: Sans-Serif Reading Experience
	   Body text shifts to sans for sustained reading.
	   Mono stays for chrome, tables, code, evidence.
	   =========================================== */

	.library-prose {
		font-family: var(--font-sans);
		font-size: var(--type-base);
		line-height: var(--leading-relaxed);
		letter-spacing: 0.005em;
		color: var(--dao-text);
		max-width: var(--content-width);
	}

	/* --- Heading Hierarchy --- */

	.library-prose :global(h1) {
		font-family: var(--font-sans);
		font-size: var(--type-2xl);
		font-weight: var(--weight-semibold);
		line-height: var(--leading-tight);
		letter-spacing: var(--tracking-tighter);
		margin-bottom: var(--space-4);
	}

	.library-prose :global(h2) {
		font-family: var(--font-sans);
		font-size: var(--type-xl);
		font-weight: var(--weight-semibold);
		line-height: var(--leading-tight);
		letter-spacing: var(--tracking-tight);
		margin-top: var(--pause-before);
		margin-bottom: var(--space-2);
	}

	.library-prose :global(h3) {
		font-family: var(--font-sans);
		font-size: var(--type-lg);
		font-weight: var(--weight-semibold);
		line-height: var(--leading-snug);
		margin-top: var(--space-4);
		margin-bottom: var(--space-1-5);
	}

	.library-prose :global(h4) {
		font-family: var(--font-sans);
		font-size: var(--type-base);
		font-weight: var(--weight-semibold);
		line-height: var(--leading-snug);
		letter-spacing: var(--tracking-wide);
		text-transform: uppercase;
		color: var(--dao-text-secondary);
		margin-top: var(--space-3);
		margin-bottom: var(--space-1);
	}

	/* --- Body Elements --- */

	.library-prose :global(p) {
		margin-bottom: var(--space-2);
	}

	.library-prose :global(ul),
	.library-prose :global(ol) {
		margin-bottom: var(--space-2);
		padding-left: var(--space-3);
	}

	.library-prose :global(li) {
		margin-bottom: var(--space-1);
	}

	/* --- Blockquotes: Research Evidence, Not Decoration --- */

	.library-prose :global(blockquote) {
		font-family: var(--font-sans);
		font-size: var(--type-base);
		font-style: normal;
		line-height: var(--leading-relaxed);
		color: var(--dao-text-secondary);
		border-left: var(--border-accent) solid var(--dao-border);
		padding-left: var(--space-3);
		margin: var(--space-3) 0;
	}

	.library-prose :global(blockquote p) {
		margin-bottom: var(--space-1);
	}

	.library-prose :global(blockquote cite),
	.library-prose :global(blockquote footer) {
		display: block;
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
		margin-top: var(--space-1);
		letter-spacing: var(--tracking-wide);
	}

	/* --- Code: Stays Monospace --- */

	.library-prose :global(pre) {
		background: var(--dao-surface);
		border: var(--border-width) solid var(--dao-border);
		border-radius: var(--radius-sm);
		padding: var(--space-2) var(--space-3);
		overflow-x: auto;
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		line-height: var(--leading-normal);
		margin: var(--space-3) 0;
	}

	.library-prose :global(code:not(pre code)) {
		font-family: var(--font-mono);
		font-size: 0.875em;
		color: var(--color-code);
		background: var(--dao-surface);
		padding: 0.1em 0.35em;
		border-radius: var(--radius-sm);
	}

	/* --- Tables: Mono Data, Sans Headers --- */

	.library-prose :global(table) {
		width: 100%;
		border-collapse: collapse;
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		line-height: var(--leading-snug);
		margin: var(--space-3) 0;
	}

	.library-prose :global(th) {
		font-family: var(--font-sans);
		font-weight: var(--weight-semibold);
		text-align: left;
		padding: var(--space-1) var(--space-2);
		border-bottom: 2px solid var(--dao-border);
		color: var(--dao-text-secondary);
		font-size: var(--type-xs);
		text-transform: uppercase;
		letter-spacing: var(--tracking-wider);
	}

	.library-prose :global(td) {
		padding: var(--space-1) var(--space-2);
		border-bottom: 1px solid var(--dao-border-subtle);
		vertical-align: top;
	}

	/* --- Horizontal Rules: Breathing Room --- */

	.library-prose :global(hr) {
		border: none;
		height: 0;
		margin: var(--rhythm-breathe) 0;
	}

	/* --- Links --- */

	.library-prose :global(a) {
		color: var(--color-link);
		text-decoration: none;
		border-bottom: 1px solid transparent;
		transition: border-color var(--duration-fast) var(--easing-linear);
	}

	.library-prose :global(a:hover) {
		border-bottom-color: var(--color-link);
	}

	/* --- Strong: Weight, Not Color --- */

	.library-prose :global(strong) {
		font-weight: var(--weight-semibold);
		color: var(--dao-text);
	}

	/* ===========================================
	   EVIDENCE LEVEL BADGES
	   Dedicated palette — brightness maps to confidence.
	   Amber for weak (not red — avoids false alarm).
	   =========================================== */

	.library-prose :global(.ev) {
		font-family: var(--font-sans);
		font-size: var(--type-xs);
		cursor: pointer;
		margin-left: 0.25ch;
		vertical-align: super;
		line-height: 1;
		transition: opacity var(--duration-fast) var(--easing-linear);
	}

	.library-prose :global(.ev:hover) {
		opacity: 1;
	}

	.library-prose :global(.ev-strong) {
		color: var(--ev-strong);
	}

	.library-prose :global(.ev-strong:hover) {
		text-shadow: 0 0 6px var(--ev-strong-bg);
	}

	.library-prose :global(.ev-moderate) {
		color: var(--ev-moderate);
	}

	.library-prose :global(.ev-moderate:hover) {
		text-shadow: 0 0 6px var(--ev-moderate-bg);
	}

	.library-prose :global(.ev-weak) {
		color: var(--ev-weak);
	}

	.library-prose :global(.ev-weak:hover) {
		text-shadow: 0 0 6px var(--ev-weak-bg);
	}

	.library-prose :global(.ev-speculative) {
		color: var(--ev-speculative);
		opacity: 0.7;
	}

	.library-prose :global(.ev-speculative:hover) {
		opacity: 0.9;
	}

	/* Keyboard focus ring for evidence badges */
	.library-prose :global(.ev:focus-visible) {
		outline: 2px solid var(--color-focus);
		outline-offset: 2px;
		border-radius: var(--radius-sm);
	}

	/* Larger touch targets on coarse pointers (mobile) */
	@media (pointer: coarse) {
		.library-prose :global(.ev) {
			padding: var(--space-0-5);
			min-width: 44px;
			min-height: 44px;
			display: inline-flex;
			align-items: center;
			justify-content: center;
		}
	}

	/* ===========================================
	   REDUCED MOTION
	   =========================================== */

	@media (prefers-reduced-motion: reduce) {
		.article-breadcrumb a,
		.article-back a {
			transition: none;
		}

		.library-prose :global(.ev) {
			transition: none;
		}
	}
</style>
