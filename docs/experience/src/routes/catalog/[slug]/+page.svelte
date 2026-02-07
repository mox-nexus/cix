<script lang="ts">
	import type { PageData } from './$types';
	import { base } from '$app/paths';
	import { marked } from 'marked';
	import { GlyphBackground } from '$lib/components/atmosphere';

	let { data }: { data: PageData } = $props();

	const variantColor: Record<string, string> = {
		spark: 'var(--spark-core)',
		emergence: 'var(--emergence-core)',
		constraint: 'var(--ci-red)'
	};

	let htmlContent = $derived(marked.parse(data.plugin.readme));

	const componentParts = $derived(
		[
			data.plugin.components.agents > 0 && `${data.plugin.components.agents} agent${data.plugin.components.agents !== 1 ? 's' : ''}`,
			data.plugin.components.skills > 0 && `${data.plugin.components.skills} skill${data.plugin.components.skills !== 1 ? 's' : ''}`,
			data.plugin.components.hooks > 0 && `${data.plugin.components.hooks} hook${data.plugin.components.hooks !== 1 ? 's' : ''}`,
			data.plugin.components.commands > 0 && `${data.plugin.components.commands} cmd${data.plugin.components.commands !== 1 ? 's' : ''}`
		].filter(Boolean) as string[]
	);
</script>

<svelte:head>
	<title>{data.plugin.slug} — cix</title>
	<meta name="description" content={data.plugin.narrativeHook || data.plugin.manifest.description} />
</svelte:head>

<GlyphBackground />

<main id="main" class="detail-page" style="--variant-color: {variantColor[data.plugin.variant]}">
	<nav class="detail-back">
		<a href="{base}/catalog">&larr; catalog</a>
	</nav>

	<header class="detail-header">
		<div class="header-top">
			<h1>{data.plugin.slug}</h1>
			<span class="detail-version">{data.plugin.manifest.version}</span>
		</div>

		{#if data.plugin.narrativeHook}
			<p class="detail-narrative">{data.plugin.narrativeHook}</p>
		{/if}

		{#if data.plugin.constraint}
			<p class="detail-constraint">Embodies: {data.plugin.constraint}</p>
		{/if}

		{#if componentParts.length > 0}
			<div class="detail-inventory">
				{#each componentParts as part}
					<span class="inv-item">{part}</span>
				{/each}
			</div>
		{/if}

		{#if data.plugin.manifest.keywords?.length}
			<div class="detail-keywords">
				{#each data.plugin.manifest.keywords as keyword}
					<span class="keyword">{keyword}</span>
				{/each}
			</div>
		{/if}
	</header>

	<article class="detail-content prose">
		{@html htmlContent}
	</article>
</main>

<style>
	.detail-page {
		min-height: 100vh;
		min-height: 100dvh;
		background: var(--dao-bg);
		padding: var(--space-3);
		padding-bottom: var(--space-4);
	}

	.detail-back {
		max-width: 72ch;
		margin: 0 auto var(--space-3);
	}

	.detail-back a {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		text-decoration: none;
		transition: color var(--duration-fast) var(--easing-linear);
	}

	.detail-back a:hover {
		color: var(--spark-core);
	}

	.detail-header {
		max-width: 72ch;
		margin: 0 auto var(--space-3);
		padding-bottom: var(--space-2);
		border-bottom: 1px solid var(--dao-border);
	}

	.header-top {
		display: flex;
		align-items: baseline;
		gap: var(--space-1);
		margin-bottom: var(--space-1);
	}

	.header-top h1 {
		font-size: var(--type-xl);
		margin: 0;
	}

	.detail-version {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
	}

	.detail-narrative {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-text-secondary);
		line-height: var(--leading-relaxed);
		margin: 0 0 var(--space-1) 0;
	}

	.detail-constraint {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--variant-color);
		margin: 0 0 var(--space-1-5) 0;
	}

	.detail-inventory {
		display: flex;
		gap: var(--space-1-5);
		flex-wrap: wrap;
		margin-bottom: var(--space-1-5);
	}

	.inv-item {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--variant-color);
	}

	.detail-keywords {
		display: flex;
		gap: var(--space-0-5);
		flex-wrap: wrap;
	}

	.keyword {
		font-family: var(--font-sans);
		font-size: var(--type-xs);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		color: var(--dao-muted);
		padding: 2px var(--space-0-5);
		border: 1px solid var(--dao-border);
		border-radius: var(--radius-sm);
	}

	/* README prose styles */
	.detail-content {
		max-width: 72ch;
		margin: 0 auto;
	}

	.prose :global(h1) {
		display: none; /* README h1 duplicates page title */
	}

	.prose :global(h2) {
		font-size: var(--type-lg);
		font-weight: 600;
		color: var(--dao-text);
		margin: var(--space-3) 0 var(--space-1) 0;
	}

	.prose :global(h3) {
		font-size: var(--type-base);
		font-weight: 600;
		color: var(--dao-text);
		margin: var(--space-2) 0 var(--space-1) 0;
	}

	.prose :global(p) {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-text-secondary);
		line-height: var(--leading-relaxed);
		margin: 0 0 var(--space-1-5) 0;
	}

	.prose :global(table) {
		width: 100%;
		border-collapse: collapse;
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		margin: var(--space-2) 0;
	}

	.prose :global(th),
	.prose :global(td) {
		padding: var(--space-0-5) var(--space-1);
		border: 1px solid var(--dao-border);
		text-align: left;
	}

	.prose :global(th) {
		color: var(--dao-text);
		background: var(--dao-surface);
	}

	.prose :global(td) {
		color: var(--dao-text-secondary);
	}

	.prose :global(code) {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		background: var(--dao-surface);
		padding: 1px 4px;
		border-radius: 2px;
	}

	.prose :global(pre) {
		background: var(--dao-surface);
		border: 1px solid var(--dao-border);
		padding: var(--space-1-5);
		overflow-x: auto;
		margin: var(--space-1-5) 0;
		border-radius: var(--radius-sm);
	}

	.prose :global(pre code) {
		background: none;
		padding: 0;
	}

	.prose :global(ul),
	.prose :global(ol) {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-text-secondary);
		padding-left: var(--space-2);
		margin: 0 0 var(--space-1-5) 0;
	}

	.prose :global(li) {
		margin-bottom: var(--space-0-5);
	}

	.prose :global(strong) {
		color: var(--dao-text);
	}

	.prose :global(a) {
		color: var(--spark-core);
		text-decoration: none;
	}

	.prose :global(a:hover) {
		text-decoration: underline;
	}

	.prose :global(blockquote) {
		border-left: 2px solid var(--variant-color);
		padding-left: var(--space-1-5);
		color: var(--dao-muted);
		margin: var(--space-1-5) 0;
	}
</style>
