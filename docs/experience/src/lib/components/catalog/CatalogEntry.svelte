<script lang="ts">
	import type { CatalogExtension } from '$lib/types/catalog';
	import { base } from '$app/paths';

	interface Props {
		extension: CatalogExtension;
		delay?: number;
	}

	let { extension, delay = 0 }: Props = $props();

	const variantColor: Record<string, string> = {
		spark: 'var(--spark-core)',
		emergence: 'var(--emergence-core)',
		constraint: 'var(--ci-red)'
	};
</script>

<a
	href="{base}/catalog/{extension.slug}"
	class="catalog-entry"
	style="--stagger-delay: {delay}ms; --variant-color: {variantColor[extension.variant]}"
>
	<div class="entry-header">
		<span class="entry-name">{extension.slug}</span>
		<span class="entry-kind">{extension.kind}</span>
		<span class="entry-version">{extension.manifest.version}</span>
	</div>
	<p class="entry-description">{extension.manifest.description}</p>
</a>

<style>
	.catalog-entry {
		display: block;
		padding: var(--space-2) var(--space-3);
		border: 1px solid var(--dao-border);
		border-left: 3px solid var(--variant-color);
		background: var(--dao-surface);
		text-decoration: none;
		color: inherit;
		cursor: pointer;

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

	@media (prefers-reduced-motion: reduce) {
		.catalog-entry {
			opacity: 1;
			transform: none;
			animation: none;
			transition: none;
		}
	}
</style>
