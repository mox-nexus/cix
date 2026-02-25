<script lang="ts">
	import { getExplanationEntries } from '$lib/data/docs';
	import { CrossLinks } from '$lib/components/nav';
	import { base } from '$app/paths';

	const entries = getExplanationEntries();
</script>

<svelte:head>
	<title>Docs — cix</title>
	<meta
		name="description"
		content="AI makes you faster now and weaker later. Both are measured. The research behind collaborative intelligence — and what design can do about it."
	/>
</svelte:head>

<div class="library-landing">
	<!-- Door 1: The Universal — TL;DR -->
	<header class="tldr">
		<h1 class="tldr-heading">AI is meant to amplify the human mind.</h1>
		<p class="tldr-lead">
			Is it substituting yours?
		</p>
		<p class="tldr-sub">
			The productivity gains are real. But productivity and capability are different buckets.
			Productivity over time depends on compounding capability. Capability atrophy leads to diminishing returns.
		</p>
		<p class="tldr-body">
			Developers thought AI made them <span class="num">24%</span> faster. It made them
			<span class="num">19%</span> slower — a <span class="num">43-point</span> gap between
			perception and reality. The more people trust AI, the less they think.
		</p>
		<p class="tldr-body">
			Productivity is up — <span class="num">26%</span> more tasks across 4,867 developers. But
			productivity and capability aren't the same thing. One rises while the other falls. The
			person it's happening to can't tell the difference.
		</p>
		<p class="tldr-body">
			When AI generates, you evaluate instead of constructing. The thinking that builds
			understanding never happens. Students who learned with AI dropped
			<span class="num">17%</span> below the control group once it was taken away.
		</p>
		<p class="tldr-lever">
			But a tutor that gave hints instead of answers eliminated the harm. Same model. Different
			design. That's what these docs are about.
		</p>
		<p class="tldr-coda">
			Whether your tools are designed this way is, as yet, unmeasured.
		</p>
	</header>

	<nav class="articles" aria-label="Articles">
		{#each entries as entry, i}
			<a href="{base}/docs/{entry.slug}" class="article-card">
				<span class="article-num">{String(i + 1).padStart(2, '0')}</span>
				<div class="article-content">
					<span class="article-title">{entry.title}</span>
					<span class="article-desc">{entry.description}</span>
				</div>
				{#if i === 0}
					<span class="article-start" aria-hidden="true">&rarr;</span>
				{/if}
			</a>
			{#if i < entries.length - 1}
				<div class="article-connector" aria-hidden="true"></div>
			{/if}
		{/each}
		<p class="articles-meta">{entries.length} articles · ~30 min · full citations</p>
	</nav>

	<CrossLinks />
</div>

<style>
	.library-landing {
		max-width: 72ch;
		margin: 0 auto;
	}

	/* ===========================================
	   TL;DR — Door 1: The Universal
	   =========================================== */

	.tldr {
		font-family: var(--font-sans);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-5);
	}

	.tldr-heading {
		font-family: var(--font-sans);
		font-size: var(--type-xl);
		font-weight: var(--weight-bold);
		line-height: var(--leading-tight);
		color: var(--constraint-core);
		margin: 0 0 var(--space-3) 0;
	}

	.tldr-lead {
		font-size: var(--type-lg);
		font-weight: var(--weight-semibold);
		line-height: var(--leading-snug);
		color: var(--spark-core);
		margin: 0 0 var(--space-1) 0;
	}

	.tldr-sub {
		font-size: var(--type-base);
		color: var(--spark-core);
		margin: 0 0 var(--space-3) 0;
	}

	.tldr-body {
		font-size: var(--type-base);
		color: var(--dao-text-secondary);
		margin: 0 0 var(--space-2) 0;
	}

	.tldr :global(.num) {
		color: var(--spark-core);
	}

	.tldr-lever {
		font-size: var(--type-base);
		color: var(--emergence-core);
		margin: 0 0 var(--space-2) 0;
	}

	.tldr-coda {
		font-family: var(--font-sans);
		font-size: var(--type-base);
		font-style: italic;
		color: var(--dao-text-secondary);
		margin: var(--space-3) 0 0 0;
	}

	/* ===========================================
	   ARTICLE CARDS — sequential argument
	   =========================================== */

	.articles {
		margin-bottom: var(--space-5);
	}

	.article-card {
		display: flex;
		align-items: flex-start;
		gap: var(--space-2);
		padding: var(--space-2) var(--space-1);
		text-decoration: none;
		border-radius: var(--radius-sm);
		transition: background var(--duration-fast) var(--easing-linear);
	}

	.article-card:hover {
		background: var(--dao-surface);
	}

	.article-num {
		font-family: var(--font-mono);
		font-size: var(--type-lg);
		font-weight: 700;
		color: var(--spark-core);
		min-width: 2.5ch;
		line-height: 1.2;
	}

	.article-content {
		display: flex;
		flex-direction: column;
		gap: 2px;
		flex: 1;
	}

	.article-title {
		font-family: var(--font-sans);
		font-size: var(--type-base);
		font-weight: 600;
		color: var(--dao-text);
	}

	.article-desc {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		line-height: var(--leading-relaxed);
	}

	.article-start {
		font-size: var(--type-lg);
		color: var(--spark-core);
		margin-top: 2px;
	}

	.article-connector {
		width: 2px;
		height: var(--space-2);
		background: var(--dao-border);
		margin-left: calc(1.25ch + var(--space-1));
	}

	.article-card:hover + .article-connector,
	.article-connector:has(+ .article-card:hover) {
		background: var(--spark-core);
		opacity: 0.4;
	}

	.articles-meta {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
		margin: var(--space-2) 0 0 0;
		padding-left: var(--space-1);
	}

	/* ===========================================
	   REDUCED MOTION
	   =========================================== */

	@media (prefers-reduced-motion: reduce) {
		.article-card {
			transition: none;
		}
	}

	@media (pointer: coarse) {
		.article-card {
			min-height: 44px;
		}
	}
</style>
