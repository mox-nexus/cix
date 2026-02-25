<script lang="ts">
	import type { CatalogExtension } from '$lib/types/catalog';
	import { base } from '$app/paths';
	import Markdown from 'svelte-exmarkdown';
	import { plugins } from '$lib/config/markdown-plugins';

	interface Props {
		extension: CatalogExtension;
	}

	let { extension }: Props = $props();

	const variantColor: Record<string, string> = {
		spark: 'var(--spark-core)',
		emergence: 'var(--emergence-core)',
		constraint: 'var(--ci-red)'
	};

	const badges = $derived(
		[
			extension.components.agents > 0 && {
				count: extension.components.agents,
				label: `agent${extension.components.agents !== 1 ? 's' : ''}`
			},
			extension.components.skills > 0 && {
				count: extension.components.skills,
				label: `skill${extension.components.skills !== 1 ? 's' : ''}`
			},
			extension.components.hooks > 0 && {
				count: extension.components.hooks,
				label: `hook${extension.components.hooks !== 1 ? 's' : ''}`
			},
			extension.components.commands > 0 && {
				count: extension.components.commands,
				label: `command${extension.components.commands !== 1 ? 's' : ''}`
			}
		].filter(Boolean) as Array<{ count: number; label: string }>
	);

	const installCmd = $derived(`cix add ${extension.slug}`);
	let copied = $state(false);

	async function copyInstall() {
		await navigator.clipboard.writeText(installCmd);
		copied = true;
		setTimeout(() => (copied = false), 1500);
	}

	// Strip the h1 and tagline from the README since we show them in the header.
	// Tagline is the first non-empty line after h1 (plain text or > blockquote).
	const readmeContent = $derived(
		extension.readme.replace(/^#\s+.+\n+(?:>\s*.+|(?!#)[^\n]+)\n/, '')
	);
</script>

<main class="plugin-detail" style="--variant-color: {variantColor[extension.variant]}">
	<nav class="back-nav">
		<a href="{base}/catalog" class="back-link">&larr; catalog</a>
	</nav>

	<header class="plugin-header">
		<div class="title-row">
			<h1 class="plugin-name">{extension.slug}</h1>
			<span class="plugin-kind">{extension.kind}</span>
			<span class="plugin-version">{extension.manifest.version}</span>
		</div>
		{#if extension.tagline}
			<p class="plugin-tagline">{extension.tagline}</p>
		{/if}
	</header>

	{#if badges.length > 0}
		<div class="component-badges">
			{#each badges as badge}
				<span class="badge">
					<span class="badge-count">{badge.count}</span>
					<span class="badge-label">{badge.label}</span>
				</span>
			{/each}
		</div>
	{/if}

	<div class="install-bar">
		<code class="install-cmd">{installCmd}</code>
		<button class="copy-btn" onclick={copyInstall} aria-label="Copy install command">
			{copied ? 'copied' : 'copy'}
		</button>
	</div>

	<hr class="divider" />

	<article class="plugin-readme">
		<Markdown md={readmeContent} {plugins} />
	</article>
</main>

<style>
	.plugin-detail {
		min-height: 100vh;
		min-height: 100dvh;
		padding: var(--space-4) var(--space-3);
		padding-bottom: var(--space-4);
		max-width: 72ch;
		margin: 0 auto;
	}

	.back-nav {
		margin-bottom: var(--space-3);
	}

	.back-link {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		text-decoration: none;
		transition: color var(--duration-fast) var(--easing-linear);
	}

	.back-link:hover {
		color: var(--variant-color);
	}

	.plugin-header {
		margin-bottom: var(--space-2);
	}

	.title-row {
		display: flex;
		align-items: baseline;
		gap: var(--space-1);
		flex-wrap: wrap;
	}

	.plugin-name {
		font-family: var(--font-sans);
		font-size: var(--type-2xl);
		font-weight: 600;
		color: var(--dao-text);
		margin: 0;
	}

	.plugin-kind {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--variant-color);
		border: 1px solid var(--variant-color);
		padding: 0 0.5ch;
		line-height: 1.6;
	}

	.plugin-version {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
	}

	.plugin-tagline {
		font-family: var(--font-mono);
		font-size: var(--type-base);
		color: var(--dao-text-secondary);
		line-height: var(--leading-relaxed);
		margin: var(--space-0-5) 0 0;
	}

	.component-badges {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-1);
		margin-bottom: var(--space-2);
	}

	.badge {
		display: inline-flex;
		align-items: baseline;
		gap: 0.3ch;
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		border: 1px solid var(--dao-border);
		padding: var(--space-0-5) var(--space-1);
	}

	.badge-count {
		color: var(--variant-color);
		font-weight: 600;
	}

	.badge-label {
		color: var(--dao-text-secondary);
	}

	.install-bar {
		display: flex;
		align-items: center;
		gap: var(--space-1);
		background: var(--dao-surface);
		border: 1px solid var(--dao-border);
		padding: var(--space-1) var(--space-2);
		margin-bottom: var(--space-3);
	}

	.install-cmd {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-text);
		flex: 1;
		user-select: all;
	}

	.copy-btn {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--variant-color);
		background: none;
		border: 1px solid var(--variant-color);
		padding: 2px var(--space-1);
		cursor: pointer;
		transition: background var(--duration-fast) var(--easing-linear);
		min-width: 5ch;
	}

	.copy-btn:hover {
		background: oklch(50% 0.1 260 / 0.1);
	}

	.divider {
		border: none;
		border-top: 1px solid var(--dao-border);
		margin: 0 0 var(--space-3);
	}

	/* README content styling — matches existing dialog-readme patterns */
	.plugin-readme :global(h1) {
		display: none;
	}

	.plugin-readme :global(h2) {
		font-family: var(--font-sans);
		font-size: var(--type-base);
		font-weight: 600;
		color: var(--dao-text);
		margin: var(--space-3) 0 var(--space-1);
	}

	.plugin-readme :global(h3) {
		font-family: var(--font-sans);
		font-size: var(--type-sm);
		font-weight: 600;
		color: var(--dao-text);
		margin: var(--space-2) 0 var(--space-0-5);
	}

	.plugin-readme :global(p) {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-text-secondary);
		line-height: var(--leading-relaxed);
		margin: 0 0 var(--space-1);
	}

	.plugin-readme :global(ul),
	.plugin-readme :global(ol) {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-text-secondary);
		line-height: var(--leading-relaxed);
		margin: 0 0 var(--space-1);
		padding-left: var(--space-3);
	}

	.plugin-readme :global(code) {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		background: var(--dao-surface-2);
		padding: 1px 4px;
	}

	.plugin-readme :global(pre) {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		background: var(--dao-surface);
		border: 1px solid var(--dao-border-subtle);
		padding: var(--space-1) var(--space-2);
		overflow-x: auto;
		margin: 0 0 var(--space-1);
	}

	.plugin-readme :global(pre code) {
		background: none;
		padding: 0;
	}

	.plugin-readme :global(strong) {
		color: var(--dao-text);
		font-weight: 600;
	}

	.plugin-readme :global(a) {
		color: var(--variant-color);
		text-decoration: none;
	}

	.plugin-readme :global(a:hover) {
		text-decoration: underline;
	}

	.plugin-readme :global(table) {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		border-collapse: collapse;
		width: 100%;
		margin: 0 0 var(--space-1);
	}

	.plugin-readme :global(th),
	.plugin-readme :global(td) {
		border: 1px solid var(--dao-border-subtle);
		padding: var(--space-0-5) var(--space-1);
		text-align: left;
	}

	.plugin-readme :global(th) {
		color: var(--dao-text);
		background: var(--dao-surface);
	}

	.plugin-readme :global(td) {
		color: var(--dao-text-secondary);
	}

	.plugin-readme :global(blockquote) {
		border-left: 2px solid var(--variant-color);
		margin: 0 0 var(--space-1);
		padding: var(--space-0-5) var(--space-2);
		color: var(--dao-text-secondary);
	}

	.plugin-readme :global(hr) {
		border: none;
		border-top: 1px solid var(--dao-border-subtle);
		margin: var(--space-2) 0;
	}

	@media (prefers-reduced-motion: reduce) {
		.back-link,
		.copy-btn {
			transition: none;
		}
	}
</style>
