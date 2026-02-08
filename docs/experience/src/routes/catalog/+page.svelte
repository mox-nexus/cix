<script lang="ts">
	import type { PageData } from './$types';
	import { CatalogEntry } from '$lib/components/catalog';
	import { CrossLinks } from '$lib/components/nav';

	let { data }: { data: PageData } = $props();
</script>

<svelte:head>
	<title>Catalog — cix</title>
	<meta name="description" content="Cognitive extensions for collaborative intelligence. {data.plugins.length} published extensions." />
</svelte:head>

<main id="main" class="catalog-page">
	<header class="catalog-header">
		<h1>Extensions</h1>
		<p class="intro">
			{data.plugins.length} cognitive extensions. Each grounded in research,
			each designed to amplify — not replace — human capability.
		</p>
	</header>

	<div class="catalog-stack">
		{#each data.plugins as plugin, i}
			<CatalogEntry {plugin} delay={i * 80} />
		{/each}
	</div>

	<CrossLinks />
</main>

<style>
	.catalog-page {
		min-height: 100vh;
		min-height: 100dvh;
		background: var(--dao-bg);
		padding: var(--space-4) var(--space-3);
		padding-bottom: var(--space-4);
	}

	.catalog-header {
		max-width: 72ch;
		margin: 0 auto var(--space-3);
	}

	.catalog-header h1 {
		font-size: var(--type-xl);
		margin: 0 0 var(--space-1) 0;
	}

	.intro {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		line-height: var(--leading-relaxed);
		margin: 0;
	}

	.catalog-stack {
		display: flex;
		flex-direction: column;
		gap: var(--space-2);
		max-width: 72ch;
		margin: 0 auto;
	}
</style>
