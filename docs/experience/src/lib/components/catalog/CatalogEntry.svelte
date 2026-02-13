<script lang="ts">
	import type { CatalogExtension } from '$lib/types/catalog';
	import { base } from '$app/paths';

	interface Props {
		extension: CatalogExtension;
		delay?: number;
	}

	let { extension, delay = 0 }: Props = $props();
	let expanded = $state(false);

	const variantColor: Record<string, string> = {
		spark: 'var(--spark-core)',
		emergence: 'var(--emergence-core)',
		constraint: 'var(--ci-red)'
	};

	const componentParts = $derived(
		[
			extension.components.agents > 0 &&
				`${extension.components.agents} agent${extension.components.agents !== 1 ? 's' : ''}`,
			extension.components.skills > 0 &&
				`${extension.components.skills} skill${extension.components.skills !== 1 ? 's' : ''}`,
			extension.components.hooks > 0 &&
				`${extension.components.hooks} hook${extension.components.hooks !== 1 ? 's' : ''}`,
			extension.components.commands > 0 &&
				`${extension.components.commands} cmd${extension.components.commands !== 1 ? 's' : ''}`
		].filter(Boolean) as string[]
	);
</script>

<!-- Layer 1: Collapsed card -->
<div
	class="catalog-entry"
	class:expanded
	style="--stagger-delay: {delay}ms; --variant-color: {variantColor[extension.variant]}"
>
	<button
		class="entry-toggle"
		onclick={() => (expanded = !expanded)}
		aria-expanded={expanded}
	>
		<div class="entry-header">
			<span class="entry-name">{extension.slug}</span>
			<span class="entry-kind">{extension.kind}</span>
			<span class="entry-version">{extension.manifest.version}</span>
		</div>
		<p class="entry-description">{extension.manifest.description}</p>
	</button>

	<!-- Layer 2: Expanded detail -->
	{#if expanded}
		<div class="entry-detail">
			{#if extension.tagline && extension.tagline !== extension.manifest.description}
				<p class="entry-tagline">{extension.tagline}</p>
			{/if}

			{#if componentParts.length > 0}
				<div class="entry-components">
					{#each componentParts as part}
						<span class="component-badge">{part}</span>
					{/each}
				</div>
			{/if}

			{#if extension.tags.length > 0}
				<div class="entry-tags">
					{#each extension.tags as tag}
						<span class="tag">{tag}</span>
					{/each}
				</div>
			{/if}

			<div class="entry-actions">
				{#if extension.docCount > 0}
					<span class="doc-count">{extension.docCount} doc{extension.docCount !== 1 ? 's' : ''}</span>
				{/if}
				<a href="{base}/catalog/{extension.slug}" class="entry-docs-link">
					open docs &rarr;
				</a>
			</div>
		</div>
	{/if}
</div>

<style>
	.catalog-entry {
		border: 1px solid var(--dao-border);
		border-left: 3px solid var(--variant-color);
		background: var(--dao-surface);

		opacity: 0;
		transform: translateY(16px);
		animation: entry-appear 500ms var(--easing-smooth) forwards;
		animation-delay: var(--stagger-delay, 0ms);
		transition: border-color var(--duration-fast) var(--easing-linear);
	}

	@keyframes entry-appear {
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.catalog-entry:hover {
		border-color: var(--variant-color);
	}

	.entry-toggle {
		display: block;
		width: 100%;
		padding: var(--space-2) var(--space-3);
		background: none;
		border: none;
		cursor: pointer;
		text-align: left;
		color: inherit;
		font: inherit;
	}

	.entry-header {
		display: flex;
		align-items: baseline;
		gap: var(--space-1);
		margin-bottom: var(--space-0-5);
	}

	.entry-name {
		font-family: var(--font-sans);
		font-size: var(--type-base);
		font-weight: 600;
		color: var(--dao-text);
	}

	.entry-kind {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--variant-color);
		border: 1px solid var(--variant-color);
		padding: 0 0.5ch;
		line-height: 1.6;
	}

	.entry-version {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
		margin-left: auto;
	}

	.entry-description {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-text-secondary);
		line-height: var(--leading-relaxed);
		margin: 0;
	}

	/* Layer 2: Expanded */
	.entry-detail {
		padding: 0 var(--space-3) var(--space-2);
		border-top: 1px solid var(--dao-border-subtle);
	}

	.entry-tagline {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-text);
		line-height: var(--leading-relaxed);
		margin: var(--space-1) 0;
	}

	.entry-components {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-1);
		margin: var(--space-1) 0;
	}

	.component-badge {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
		background: var(--dao-surface-2);
		padding: 2px var(--space-1);
	}

	.entry-tags {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-0-5);
		margin: var(--space-1) 0;
	}

	.tag {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
		border: 1px solid var(--dao-border-subtle);
		padding: 1px var(--space-0-5);
	}

	.entry-actions {
		display: flex;
		align-items: baseline;
		gap: var(--space-1-5);
		margin-top: var(--space-1);
	}

	.doc-count {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
	}

	.entry-docs-link {
		display: inline-block;
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--variant-color);
		text-decoration: none;
		transition: opacity var(--duration-fast) var(--easing-linear);
	}

	.entry-docs-link:hover {
		opacity: 0.8;
	}

	@media (prefers-reduced-motion: reduce) {
		.catalog-entry {
			opacity: 1;
			transform: none;
			animation: none;
		}

		.entry-docs-link {
			transition: none;
		}
	}
</style>
