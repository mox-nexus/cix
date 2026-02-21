<script lang="ts">
	import type { CatalogExtension } from '$lib/types/catalog';
	import { marked } from 'marked';

	interface Props {
		extension: CatalogExtension;
		delay?: number;
	}

	let { extension, delay = 0 }: Props = $props();

	let dialogEl: HTMLDialogElement | undefined = $state();

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

	const readmeHtml = $derived(marked.parse(extension.readme) as string);

	function openDialog() {
		dialogEl?.showModal();
	}

	function closeDialog() {
		dialogEl?.close();
	}
</script>

<!-- Card -->
<div
	class="catalog-entry"
	style="--stagger-delay: {delay}ms; --variant-color: {variantColor[extension.variant]}"
>
	<button class="entry-toggle" onclick={openDialog}>
		<div class="entry-header">
			<span class="entry-name">{extension.slug}</span>
			<span class="entry-kind">{extension.kind}</span>
			<span class="entry-version">{extension.manifest.version}</span>
		</div>
		<p class="entry-description">{extension.manifest.description}</p>
	</button>
</div>

<!-- Holographic dialog -->
<dialog
	bind:this={dialogEl}
	class="readme-dialog"
	style="--variant-color: {variantColor[extension.variant]}"
	onclick={(e) => { if (e.target === dialogEl) closeDialog(); }}
>
	<div class="dialog-chrome">
		<header class="dialog-header">
			<div class="dialog-title-row">
				<h2 class="dialog-name">{extension.slug}</h2>
				<span class="dialog-kind">{extension.kind}</span>
				<span class="dialog-version">{extension.manifest.version}</span>
			</div>
			<button class="dialog-close" onclick={closeDialog} aria-label="Close">&times;</button>
		</header>

		{#if componentParts.length > 0}
			<div class="dialog-components">
				{#each componentParts as part}
					<span class="component-badge">{part}</span>
				{/each}
			</div>
		{/if}

		<article class="dialog-readme">
			{@html readmeHtml}
		</article>
	</div>
</dialog>

<style>
	/* Card styles */
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

	/* Dialog styles */
	.readme-dialog {
		border: none;
		background: transparent;
		padding: 0;
		max-width: min(72ch, 90vw);
		max-height: 85vh;
		width: 100%;
		margin: auto;
		overflow: visible;
	}

	.readme-dialog::backdrop {
		background: oklch(8% 0.02 260 / 0.85);
		backdrop-filter: blur(8px);
	}

	.readme-dialog[open] {
		animation: dialog-enter 200ms var(--easing-smooth);
	}

	@keyframes dialog-enter {
		from {
			opacity: 0;
			transform: scale(0.97) translateY(8px);
		}
	}

	.dialog-chrome {
		background: var(--dao-bg);
		border: 1px solid var(--variant-color);
		box-shadow:
			0 0 40px oklch(50% 0.15 260 / 0.15),
			inset 0 1px 0 oklch(100% 0 0 / 0.03);
		overflow: hidden;
		display: flex;
		flex-direction: column;
		max-height: 85vh;
	}

	.dialog-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: var(--space-2) var(--space-3);
		border-bottom: 1px solid var(--dao-border);
	}

	.dialog-title-row {
		display: flex;
		align-items: baseline;
		gap: var(--space-1);
	}

	.dialog-name {
		font-family: var(--font-sans);
		font-size: var(--type-lg);
		font-weight: 600;
		color: var(--dao-text);
		margin: 0;
	}

	.dialog-kind {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--variant-color);
		border: 1px solid var(--variant-color);
		padding: 0 0.5ch;
		line-height: 1.6;
	}

	.dialog-version {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
	}

	.dialog-close {
		background: none;
		border: none;
		color: var(--dao-muted);
		font-size: var(--type-xl);
		cursor: pointer;
		padding: 0 var(--space-0-5);
		line-height: 1;
		transition: color var(--duration-fast) var(--easing-linear);
	}

	.dialog-close:hover {
		color: var(--dao-text);
	}

	.dialog-components {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-1);
		padding: var(--space-1) var(--space-3);
		border-bottom: 1px solid var(--dao-border-subtle);
	}

	.component-badge {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--variant-color);
	}

	/* README content */
	.dialog-readme {
		padding: var(--space-2) var(--space-3);
		overflow-y: auto;
		flex: 1;
		min-height: 0;
	}

	.dialog-readme :global(h1) {
		display: none;
	}

	.dialog-readme :global(h2) {
		font-family: var(--font-sans);
		font-size: var(--type-base);
		font-weight: 600;
		color: var(--dao-text);
		margin: var(--space-2) 0 var(--space-1);
	}

	.dialog-readme :global(h3) {
		font-family: var(--font-sans);
		font-size: var(--type-sm);
		font-weight: 600;
		color: var(--dao-text);
		margin: var(--space-1-5) 0 var(--space-0-5);
	}

	.dialog-readme :global(p) {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-text-secondary);
		line-height: var(--leading-relaxed);
		margin: 0 0 var(--space-1);
	}

	.dialog-readme :global(ul),
	.dialog-readme :global(ol) {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-text-secondary);
		line-height: var(--leading-relaxed);
		margin: 0 0 var(--space-1);
		padding-left: var(--space-3);
	}

	.dialog-readme :global(code) {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		background: var(--dao-surface-2);
		padding: 1px 4px;
	}

	.dialog-readme :global(pre) {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		background: var(--dao-surface);
		border: 1px solid var(--dao-border-subtle);
		padding: var(--space-1) var(--space-2);
		overflow-x: auto;
		margin: 0 0 var(--space-1);
	}

	.dialog-readme :global(pre code) {
		background: none;
		padding: 0;
	}

	.dialog-readme :global(strong) {
		color: var(--dao-text);
		font-weight: 600;
	}

	.dialog-readme :global(a) {
		color: var(--variant-color);
		text-decoration: none;
	}

	.dialog-readme :global(a:hover) {
		text-decoration: underline;
	}

	.dialog-readme :global(table) {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		border-collapse: collapse;
		width: 100%;
		margin: 0 0 var(--space-1);
	}

	.dialog-readme :global(th),
	.dialog-readme :global(td) {
		border: 1px solid var(--dao-border-subtle);
		padding: var(--space-0-5) var(--space-1);
		text-align: left;
	}

	.dialog-readme :global(th) {
		color: var(--dao-text);
		background: var(--dao-surface);
	}

	.dialog-readme :global(td) {
		color: var(--dao-text-secondary);
	}

	.dialog-readme :global(blockquote) {
		border-left: 2px solid var(--variant-color);
		margin: 0 0 var(--space-1);
		padding: var(--space-0-5) var(--space-2);
		color: var(--dao-text-secondary);
	}

	.dialog-readme :global(hr) {
		border: none;
		border-top: 1px solid var(--dao-border-subtle);
		margin: var(--space-2) 0;
	}

	@media (prefers-reduced-motion: reduce) {
		.catalog-entry {
			opacity: 1;
			transform: none;
			animation: none;
		}

		.readme-dialog[open] {
			animation: none;
		}

		.dialog-close {
			transition: none;
		}
	}
</style>
