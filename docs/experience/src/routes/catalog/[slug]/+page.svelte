<script lang="ts">
	import type { PageData } from './$types';
	import { base } from '$app/paths';
	import { marked } from 'marked';

	let { data }: { data: PageData } = $props();

	const variantColor: Record<string, string> = {
		spark: 'var(--spark-core)',
		emergence: 'var(--emergence-core)',
		constraint: 'var(--ci-red)'
	};

	let htmlContent = $derived(marked.parse(data.extension.readme));

	const componentParts = $derived(
		[
			data.extension.components.agents > 0 &&
				`${data.extension.components.agents} agent${data.extension.components.agents !== 1 ? 's' : ''}`,
			data.extension.components.skills > 0 &&
				`${data.extension.components.skills} skill${data.extension.components.skills !== 1 ? 's' : ''}`,
			data.extension.components.hooks > 0 &&
				`${data.extension.components.hooks} hook${data.extension.components.hooks !== 1 ? 's' : ''}`,
			data.extension.components.commands > 0 &&
				`${data.extension.components.commands} cmd${data.extension.components.commands !== 1 ? 's' : ''}`
		].filter(Boolean) as string[]
	);
</script>

<svelte:head>
	<title>{data.extension.slug} — cix</title>
	<meta name="description" content={data.extension.manifest.description} />
</svelte:head>

<main
	id="main"
	class="detail-page"
	style="--variant-color: {variantColor[data.extension.variant]}"
>
	<nav class="detail-back">
		<a href="{base}/catalog">&larr; catalog</a>
	</nav>

	<header class="detail-header">
		<div class="header-top">
			<h1>{data.extension.slug}</h1>
			<span class="detail-kind">{data.extension.kind}</span>
			<span class="detail-version">{data.extension.manifest.version}</span>
		</div>

		<p class="detail-description">{data.extension.manifest.description}</p>

		{#if componentParts.length > 0}
			<div class="detail-inventory">
				{#each componentParts as part}
					<span class="inv-item">{part}</span>
				{/each}
			</div>
		{/if}

		{#if data.extension.tags.length > 0}
			<div class="detail-tags">
				{#each data.extension.tags as tag}
					<span class="tag">{tag}</span>
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

	.detail-kind {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--variant-color);
		border: 1px solid var(--variant-color);
		padding: 0 0.5ch;
		line-height: 1.6;
	}

	.detail-version {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		margin-left: auto;
	}

	.detail-description {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-text-secondary);
		line-height: var(--leading-relaxed);
		margin: 0 0 var(--space-1) 0;
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

	.detail-tags {
		display: flex;
		gap: var(--space-0-5);
		flex-wrap: wrap;
	}

	.tag {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
		border: 1px solid var(--dao-border-subtle);
		padding: 1px var(--space-0-5);
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
