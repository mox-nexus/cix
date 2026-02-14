<script lang="ts">
	import type { PageData } from './$types';
	import type { DocCategory } from '$lib/types/catalog';
	import { base } from '$app/paths';
	import { marked } from 'marked';
	import { onMount, tick } from 'svelte';

	let { data }: { data: PageData } = $props();

	const variantColor: Record<string, string> = {
		spark: 'var(--spark-core)',
		emergence: 'var(--emergence-core)',
		constraint: 'var(--ci-red)'
	};

	// Custom marked renderer: emit mermaid blocks as <pre class="mermaid">
	const renderer = new marked.Renderer();
	const originalCode = renderer.code.bind(renderer);
	renderer.code = function (token: { text: string; lang?: string }) {
		if (token.lang === 'mermaid') {
			return `<pre class="mermaid">${token.text}</pre>`;
		}
		return originalCode(token);
	};
	marked.use({ renderer });

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

	// Doc tabs
	const TAB_LABELS: Record<string, string> = {
		readme: 'README',
		explanation: 'Explanation',
		'how-to': 'How-To',
		tutorials: 'Tutorials'
	};

	const docs = data.extension.docs;
	const availableTabs = $derived(() => {
		const tabs = ['readme'];
		if (!docs) return tabs;
		for (const cat of ['explanation', 'how-to', 'tutorials'] as DocCategory[]) {
			if (docs[cat].length > 0) tabs.push(cat);
		}
		return tabs;
	});
	const hasTabs = $derived(availableTabs().length > 1);

	let activeTab = $state('readme');
	let mounted = $state(false);
	let contentEl: HTMLElement | undefined = $state();

	function docHtml(category: DocCategory): string {
		if (!docs) return '';
		return docs[category]
			.map((entry) => marked.parse(entry.content))
			.join('<hr class="doc-separator" />');
	}

	async function renderMermaid(container: HTMLElement) {
		const els = container.querySelectorAll<HTMLElement>('pre.mermaid');
		if (els.length === 0) return;

		const { default: mermaid } = await import('mermaid');
		mermaid.initialize({
			startOnLoad: false,
			theme: 'base',
			themeVariables: {
				darkMode: true,
				background: '#1a1b2e',
				primaryColor: '#252640',
				primaryTextColor: '#e0e1ec',
				primaryBorderColor: '#2e3050',
				secondaryColor: '#2e3050',
				secondaryTextColor: '#b0b1c4',
				secondaryBorderColor: '#2e3050',
				tertiaryColor: '#16172a',
				tertiaryTextColor: '#b0b1c4',
				tertiaryBorderColor: '#252640',
				lineColor: '#4d6080',
				textColor: '#e0e1ec',
				noteBkgColor: '#252640',
				noteTextColor: '#b0b1c4',
				noteBorderColor: '#2e3050',
				fontFamily: "'IBM Plex Mono', ui-monospace, monospace",
				fontSize: '14px',
				nodeBorder: '#2e3050',
				clusterBkg: '#1e1f30',
				clusterBorder: '#2e3050',
				defaultLinkColor: '#4d6080',
				edgeLabelBackground: '#1a1b2e',
				actorBkg: '#252640',
				actorBorder: '#3a4060',
				actorTextColor: '#e0e1ec',
				signalColor: '#b0b1c4',
				signalTextColor: '#e0e1ec'
			},
			flowchart: { htmlLabels: true, curve: 'basis' },
			sequence: { mirrorActors: false, actorMargin: 80, messageFontSize: 14 }
		});
		await mermaid.run({ nodes: els });
	}

	onMount(() => {
		const hash = window.location.hash.slice(1);
		if (hash && availableTabs().includes(hash)) {
			activeTab = hash;
		}
		mounted = true;
	});

	// Render mermaid after content changes
	$effect(() => {
		// Track the reactive dependency
		const _tab = activeTab;
		if (!mounted || !contentEl) return;
		// Wait for DOM update before scanning for mermaid blocks
		tick().then(() => {
			if (contentEl) renderMermaid(contentEl);
		});
	});

	$effect(() => {
		if (!mounted) return;
		if (activeTab !== 'readme') {
			history.replaceState(null, '', `#${activeTab}`);
		} else {
			history.replaceState(null, '', window.location.pathname);
		}
	});
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

	{#if hasTabs}
		<nav class="detail-tabs" role="tablist">
			{#each availableTabs() as tab}
				<button
					role="tab"
					class="tab"
					class:active={activeTab === tab}
					aria-selected={activeTab === tab}
					onclick={() => (activeTab = tab)}
				>
					{TAB_LABELS[tab]}
					{#if tab !== 'readme' && docs}
						<span class="tab-count">{docs[tab as DocCategory].length}</span>
					{/if}
				</button>
			{/each}
		</nav>
	{/if}

	<article
		class="detail-content"
		class:prose={activeTab === 'readme'}
		class:prose-docs={activeTab !== 'readme'}
		bind:this={contentEl}
	>
		{#if activeTab === 'readme'}
			{@html htmlContent}
		{:else}
			{@html docHtml(activeTab as DocCategory)}
		{/if}
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

	/* Doc tabs */
	.detail-tabs {
		max-width: 72ch;
		margin: 0 auto var(--space-3);
		display: flex;
		gap: 0;
		border-bottom: 1px solid var(--dao-border);
	}

	.tab {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
		background: none;
		border: none;
		border-bottom: 2px solid transparent;
		padding: var(--space-0-5) var(--space-1-5);
		cursor: pointer;
		transition: color var(--duration-fast) var(--easing-linear);
	}

	.tab:hover {
		color: var(--dao-text);
	}

	.tab.active {
		color: var(--variant-color);
		border-bottom-color: var(--variant-color);
	}

	.tab-count {
		font-size: var(--type-xs);
		color: var(--dao-muted);
		margin-left: 0.3ch;
		opacity: 0.6;
	}

	/* Prose content */
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

	.prose :global(hr.doc-separator) {
		border: none;
		border-top: 1px solid var(--dao-border);
		margin: var(--space-3) 0;
	}

	/* ==========================================
	   DOCS PROSE: Sans-Serif Long-Form Reading
	   Active on Explanation / How-To / Tutorial tabs
	   ========================================== */

	.prose-docs {
		max-width: var(--content-width);
	}

	.prose-docs :global(h1) {
		font-family: var(--font-sans);
		font-size: var(--type-2xl);
		font-weight: var(--weight-semibold);
		line-height: var(--leading-tight);
		letter-spacing: var(--tracking-tighter);
		color: var(--dao-text);
		margin-top: var(--space-5);
		margin-bottom: var(--space-3);
		padding-bottom: var(--space-1);
		border-bottom: 1px solid var(--dao-border-subtle);
	}

	.prose-docs :global(h1:first-child) {
		margin-top: 0;
	}

	.prose-docs :global(h2) {
		font-family: var(--font-sans);
		font-size: var(--type-xl);
		font-weight: var(--weight-semibold);
		line-height: var(--leading-tight);
		letter-spacing: var(--tracking-tight);
		color: var(--dao-text);
		margin-top: var(--pause-before);
		margin-bottom: var(--space-2);
	}

	.prose-docs :global(h3) {
		font-family: var(--font-sans);
		font-size: var(--type-lg);
		font-weight: var(--weight-semibold);
		line-height: var(--leading-snug);
		color: var(--dao-text);
		margin-top: var(--space-4);
		margin-bottom: var(--space-1-5);
	}

	.prose-docs :global(h4) {
		font-family: var(--font-sans);
		font-size: var(--type-base);
		font-weight: var(--weight-semibold);
		line-height: var(--leading-snug);
		letter-spacing: var(--tracking-wide);
		text-transform: uppercase;
		color: var(--dao-text-secondary);
		margin-top: var(--space-3);
		margin-bottom: var(--space-1);
	}

	.prose-docs :global(p) {
		font-family: var(--font-sans);
		font-size: var(--type-base);
		color: var(--dao-text);
		line-height: 1.7;
		letter-spacing: 0.005em;
		margin: 0 0 var(--space-2) 0;
	}

	.prose-docs :global(ul),
	.prose-docs :global(ol) {
		font-family: var(--font-sans);
		font-size: var(--type-base);
		color: var(--dao-text);
		line-height: 1.7;
		letter-spacing: 0.005em;
		padding-left: var(--space-3);
		margin: 0 0 var(--space-2) 0;
	}

	.prose-docs :global(li) {
		margin-bottom: var(--space-1);
	}

	.prose-docs :global(li > ul),
	.prose-docs :global(li > ol) {
		margin-top: var(--space-1);
		margin-bottom: 0;
	}

	.prose-docs :global(strong) {
		font-weight: var(--weight-semibold);
		color: var(--dao-text);
	}

	.prose-docs :global(a) {
		color: var(--color-link);
		text-decoration: none;
		border-bottom: 1px solid transparent;
		transition: border-color var(--duration-fast) var(--easing-linear);
	}

	.prose-docs :global(a:hover) {
		border-bottom-color: var(--color-link);
	}

	/* Inline code in docs prose */
	.prose-docs :global(code:not(pre code)) {
		font-family: var(--font-mono);
		font-size: 0.875em;
		color: var(--color-code);
		background: var(--dao-surface);
		padding: 0.1em 0.35em;
		border-radius: var(--radius-sm);
	}

	.prose-docs :global(pre) {
		background: var(--dao-surface);
		border: 1px solid var(--dao-border);
		border-radius: var(--radius-sm);
		padding: var(--space-2) var(--space-3);
		overflow-x: auto;
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		line-height: var(--leading-normal);
		margin: var(--space-3) 0;
	}

	.prose-docs :global(pre code) {
		background: none;
		padding: 0;
		font-size: inherit;
		color: var(--dao-text);
	}

	/* Tables: sans headers, mono data */
	.prose-docs :global(table) {
		width: 100%;
		border-collapse: collapse;
		margin: var(--space-3) 0;
		display: block;
		overflow-x: auto;
		-webkit-overflow-scrolling: touch;
	}

	.prose-docs :global(th) {
		font-family: var(--font-sans);
		font-weight: var(--weight-semibold);
		text-align: left;
		padding: var(--space-1) var(--space-2);
		border-bottom: 2px solid var(--dao-border);
		color: var(--dao-text-secondary);
		font-size: var(--type-sm);
		text-transform: uppercase;
		letter-spacing: var(--tracking-wider);
		white-space: nowrap;
	}

	.prose-docs :global(td) {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		padding: var(--space-1) var(--space-2);
		border-bottom: 1px solid var(--dao-border-subtle);
		color: var(--dao-text-secondary);
		vertical-align: top;
		line-height: var(--leading-normal);
	}

	/* Blockquotes */
	.prose-docs :global(blockquote) {
		font-family: var(--font-sans);
		font-size: var(--type-base);
		font-style: normal;
		line-height: 1.7;
		color: var(--dao-text-secondary);
		border-left: var(--border-accent) solid var(--dao-border);
		padding-left: var(--space-3);
		margin: var(--space-3) 0;
	}

	.prose-docs :global(blockquote p) {
		margin-bottom: var(--space-1);
		color: var(--dao-text-secondary);
	}

	/* Horizontal rules */
	.prose-docs :global(hr) {
		border: none;
		height: 1px;
		background: var(--dao-border);
		margin: var(--space-4) 0;
	}

	.prose-docs :global(hr.doc-separator) {
		background: none;
		height: 0;
		margin: var(--rhythm-breathe) 0;
	}

	/* ==========================================
	   MERMAID DIAGRAMS (both prose modes)
	   ========================================== */

	.prose-docs :global(pre.mermaid),
	.prose :global(pre.mermaid) {
		background: transparent;
		border: 1px solid var(--dao-border-subtle);
		border-radius: var(--radius-sm);
		padding: var(--space-3) var(--space-2);
		margin: var(--space-3) 0;
		overflow-x: auto;
		text-align: center;
	}

	.prose-docs :global(pre.mermaid svg),
	.prose :global(pre.mermaid svg) {
		height: auto;
		display: inline-block;
	}

	@media (prefers-reduced-motion: reduce) {
		.tab,
		.prose-docs :global(a) {
			transition: none;
		}
	}
</style>
