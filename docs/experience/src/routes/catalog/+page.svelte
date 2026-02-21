<script lang="ts">
	import type { PageData } from './$types';
	import { CatalogEntry } from '$lib/components/catalog';
	import { CrossLinks } from '$lib/components/nav';

	let { data }: { data: PageData } = $props();

	let query = $state('');

	let filtered = $derived(() => {
		const q = query.toLowerCase().trim();
		if (!q) return data.extensions;
		return data.extensions.filter(
			(ext) =>
				ext.slug.includes(q) ||
				ext.tagline.toLowerCase().includes(q) ||
				ext.manifest.description.toLowerCase().includes(q) ||
				ext.kind.includes(q) ||
				ext.tags.some((t) => t.toLowerCase().includes(q))
		);
	});
</script>

<svelte:head>
	<title>Catalog — cix</title>
	<meta
		name="description"
		content="Cognitive extensions for collaborative intelligence."
	/>
</svelte:head>

<main id="main" class="catalog-page">
	<header class="catalog-header">
		<h1>Extensions</h1>
		<p class="intro">
			Cognitive extensions grounded in research, designed to amplify
			collaboration.
		</p>
	</header>

	<div class="catalog-search">
		<input
			type="text"
			bind:value={query}
			placeholder="search extensions..."
			class="search-input"
			aria-label="Search extensions"
		/>
	</div>

	<div class="catalog-stack">
		{#each filtered() as ext, i (ext.slug)}
			<CatalogEntry extension={ext} delay={i * 80} />
		{/each}
		{#if filtered().length === 0}
			<p class="no-results">No extensions match "{query}"</p>
		{/if}
	</div>

	<CrossLinks />
</main>

<style>
	.catalog-page {
		min-height: 100vh;
		min-height: 100dvh;
		padding: var(--space-4) var(--space-3);
		padding-bottom: var(--space-4);
	}

	.catalog-header {
		max-width: 72ch;
		margin: 0 auto var(--space-3);
	}

	.catalog-header h1 {
		font-size: var(--type-2xl);
		margin: 0 0 var(--space-1) 0;
	}

	.intro {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		line-height: var(--leading-relaxed);
		margin: 0;
	}

	.catalog-search {
		max-width: 72ch;
		margin: 0 auto var(--space-3);
	}

	.search-input {
		width: 100%;
		padding: var(--space-1) var(--space-2);
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-text);
		background: var(--dao-surface);
		border: 1px solid var(--dao-border);
		outline: none;
		transition: border-color var(--duration-fast) var(--easing-linear);
	}

	.search-input::placeholder {
		color: var(--dao-muted);
	}

	.search-input:focus {
		border-color: var(--spark-core);
	}

	.catalog-stack {
		display: flex;
		flex-direction: column;
		gap: var(--space-2);
		max-width: 72ch;
		margin: 0 auto;
	}

	.no-results {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		text-align: center;
		padding: var(--space-4) 0;
	}

	@media (prefers-reduced-motion: reduce) {
		.search-input {
			transition: none;
		}
	}
</style>
