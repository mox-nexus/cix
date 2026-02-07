<script lang="ts">
	import type { CatalogPlugin } from '$lib/types/catalog';

	interface Props {
		plugin: CatalogPlugin;
		delay?: number;
	}

	let { plugin, delay = 0 }: Props = $props();

	const variantColor: Record<string, string> = {
		spark: 'var(--spark-core)',
		emergence: 'var(--emergence-core)',
		constraint: 'var(--ci-red)'
	};

	const componentParts = $derived(
		[
			plugin.components.agents > 0 && `${plugin.components.agents} agent${plugin.components.agents !== 1 ? 's' : ''}`,
			plugin.components.skills > 0 && `${plugin.components.skills} skill${plugin.components.skills !== 1 ? 's' : ''}`,
			plugin.components.hooks > 0 && `${plugin.components.hooks} hook${plugin.components.hooks !== 1 ? 's' : ''}`,
			plugin.components.commands > 0 && `${plugin.components.commands} cmd${plugin.components.commands !== 1 ? 's' : ''}`
		].filter(Boolean) as string[]
	);
</script>

<a
	href="/catalog/{plugin.slug}"
	class="catalog-entry"
	style="--stagger-delay: {delay}ms; --variant-color: {variantColor[plugin.variant]}"
>
	<div class="entry-header">
		<h2 class="entry-name">{plugin.slug}</h2>
		<span class="entry-version">{plugin.manifest.version}</span>
	</div>

	<p class="entry-description">{plugin.narrativeHook || plugin.tagline}</p>

	{#if plugin.constraint}
		<p class="entry-constraint">Embodies: {plugin.constraint}</p>
	{/if}

	<div class="entry-footer">
		{#if componentParts.length > 0}
			<span class="entry-components">{componentParts.join('  ')}</span>
		{/if}
		<span class="entry-explore">Explore &rarr;</span>
	</div>
</a>

<style>
	.catalog-entry {
		display: block;
		text-decoration: none;
		border: 1px solid var(--dao-border);
		border-left: 3px solid var(--variant-color);
		padding: var(--space-2) var(--space-3);
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

	.entry-header {
		display: flex;
		align-items: baseline;
		justify-content: space-between;
		margin-bottom: var(--space-1);
	}

	.entry-name {
		font-family: var(--font-sans);
		font-size: var(--type-base);
		font-weight: 600;
		color: var(--dao-text);
		margin: 0;
	}

	.entry-version {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
	}

	.entry-description {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-text-secondary);
		line-height: var(--leading-relaxed);
		margin: 0 0 var(--space-1) 0;
	}

	.entry-constraint {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--variant-color);
		margin: 0 0 var(--space-1-5) 0;
	}

	.entry-footer {
		display: flex;
		align-items: baseline;
		justify-content: space-between;
	}

	.entry-components {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
	}

	.entry-explore {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--variant-color);
		margin-left: auto;
	}

	@media (prefers-reduced-motion: reduce) {
		.catalog-entry {
			opacity: 1;
			transform: none;
			animation: none;
		}
	}
</style>
