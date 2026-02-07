<script lang="ts">
	import { LIBRARY } from '$lib/data/library';
	import { base } from '$app/paths';
	import { ContentList } from '$lib/components/library';
	import { CrossLinks } from '$lib/components/nav';
	import { GlyphBackground } from '$lib/components/atmosphere';

	let populated = $derived(LIBRARY.filter((q) => q.entries.length > 0));
</script>

<svelte:head>
	<title>Library — cix</title>
	<meta
		name="description"
		content="Research and practice of collaborative intelligence. Understanding, learning, doing, looking up."
	/>
</svelte:head>

<GlyphBackground />

<div class="library-index">
	<header class="library-header">
		<h1>Library</h1>
		<p class="intro">
			The research behind collaborative intelligence, organized by how you
			need it: understanding, learning, doing, looking up.
		</p>
	</header>

	<nav class="diataxis-map" aria-label="Documentation sections">
		{#each populated as quadrant}
			<a
				href="#{quadrant.id}"
				class="map-link"
				style="--quadrant-color: var(--quadrant-{quadrant.variant})"
			>
				<span class="map-label">{quadrant.label}</span>
				<span class="map-count">{quadrant.entries.length}</span>
			</a>
		{/each}
	</nav>

	{#each populated as quadrant (quadrant.id)}
		<section id={quadrant.id} class="quadrant-section" style="--quadrant-color: var(--quadrant-{quadrant.variant})">
			<div class="quadrant-header">
				<h2 class="quadrant-label">{quadrant.label}</h2>
				<p class="quadrant-tagline">{quadrant.tagline}</p>
			</div>

			{#if quadrant.id === 'explanation'}
				<ContentList quadrant={quadrant.id} entries={quadrant.entries} ordered={true} />
			{:else if quadrant.id === 'reference'}
				{#each quadrant.entries as entry}
					<a href="{base}/library/reference/{entry.slug}" class="ref-link">
						<span class="ref-title">{entry.title}</span>
						<span class="ref-description">{entry.description}</span>
					</a>
				{/each}
			{:else}
				<ContentList quadrant={quadrant.id} entries={quadrant.entries} />
			{/if}
		</section>
	{/each}

	<CrossLinks />
</div>

<style>
	.library-index {
		--quadrant-spark: var(--spark-core);
		--quadrant-emergence: var(--emergence-core);
		--quadrant-muted: var(--dao-text-secondary);

		max-width: 72ch;
		margin: 0 auto;
	}

	.library-header {
		margin-bottom: var(--space-4);
	}

	.library-header h1 {
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

	/* --- Diataxis Map Strip --- */
	.diataxis-map {
		display: flex;
		gap: var(--space-3);
		padding-bottom: var(--space-2);
		border-bottom: 1px solid var(--dao-border-subtle);
		margin-bottom: var(--space-4);
		flex-wrap: wrap;
	}

	.map-link {
		font-family: var(--font-sans);
		font-size: var(--type-xs);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		color: var(--dao-muted);
		text-decoration: none;
		display: inline-flex;
		align-items: center;
		gap: var(--space-1);
		transition: color var(--duration-fast) var(--easing-linear);
	}

	.map-link::before {
		content: '';
		display: inline-block;
		width: 12px;
		height: 2px;
		background: var(--quadrant-color, var(--dao-muted));
		flex-shrink: 0;
	}

	.map-link:hover {
		color: var(--dao-text);
	}

	.map-count {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
		opacity: 0.5;
	}

	/* --- Quadrant Sections --- */
	.quadrant-section {
		margin-bottom: var(--space-4);
	}

	.quadrant-header {
		margin-bottom: var(--space-2);
		padding-bottom: var(--space-1);
		border-bottom: 1px solid var(--dao-border-subtle);
	}

	.quadrant-label {
		font-family: var(--font-sans);
		font-size: var(--type-xs);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		color: var(--quadrant-color, var(--dao-muted));
		margin: 0 0 var(--space-0-5) 0;
		display: flex;
		align-items: center;
		gap: var(--space-1);
		font-weight: 600;
	}

	.quadrant-label::before {
		content: '';
		display: inline-block;
		width: 16px;
		height: 2px;
		background: var(--quadrant-color, var(--dao-muted));
		flex-shrink: 0;
	}

	.quadrant-tagline {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		margin: 0;
		line-height: var(--leading-relaxed);
	}

	/* --- Reference Link --- */
	.ref-link {
		display: block;
		padding: var(--space-2);
		background: var(--dao-surface);
		border: 1px solid var(--dao-border);
		border-left: 3px solid var(--quadrant-color, var(--dao-text-secondary));
		border-radius: var(--radius-sm);
		text-decoration: none;
		transition: border-color var(--duration-fast) var(--easing-linear);
	}

	.ref-link:hover {
		border-color: var(--quadrant-color, var(--dao-text-secondary));
	}

	.ref-title {
		display: block;
		font-family: var(--font-sans);
		font-size: var(--type-base);
		font-weight: 600;
		color: var(--dao-text);
		margin-bottom: 2px;
	}

	.ref-description {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
	}

	@media (prefers-reduced-motion: reduce) {
		.map-link,
		.ref-link {
			transition: none;
		}
	}
</style>
