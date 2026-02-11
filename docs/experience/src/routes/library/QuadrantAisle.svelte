<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		id: string;
		label: string;
		tagline: string;
		count: number;
		expanded: boolean;
		ontoggle: () => void;
		preview?: string;
		progress?: { completed: number; total: number };
		placeholder?: boolean;
		variant?: string;
		delay?: number;
		content?: Snippet;
	}

	let {
		id,
		label,
		tagline,
		count,
		expanded,
		ontoggle,
		preview,
		progress,
		placeholder = false,
		variant = 'explanation',
		delay = 0,
		content
	}: Props = $props();

	const VARIANT_COLOR: Record<string, string> = {
		explanation: 'var(--quadrant-explanation)',
		'how-to': 'var(--quadrant-how-to)',
		tutorials: 'var(--quadrant-tutorials)',
		reference: 'var(--quadrant-reference)'
	};

	let variantColor = $derived(VARIANT_COLOR[variant] ?? 'var(--dao-muted)');
	let progressPct = $derived(
		progress && progress.total > 0 ? (progress.completed / progress.total) * 100 : 0
	);
</script>

<section
	{id}
	class="aisle"
	class:expanded
	class:placeholder
	style="--stagger-delay: {delay}ms; --variant-color: {variantColor}"
>
	<button
		class="aisle-toggle"
		onclick={ontoggle}
		aria-expanded={expanded}
		disabled={placeholder}
	>
		<div class="aisle-header">
			<h2 class="aisle-label">{label}</h2>
			<span class="aisle-count">{count} {count === 1 ? 'article' : 'articles'}</span>
			{#if !placeholder}
				<span class="aisle-chevron" aria-hidden="true">{expanded ? '\u25BE' : '\u25B8'}</span>
			{/if}
		</div>
		<p class="aisle-tagline">{tagline}</p>
		{#if preview && !expanded}
			<p class="aisle-preview">{preview}</p>
		{/if}
		{#if progress && progress.total > 0 && !expanded}
			<div class="aisle-progress" aria-label="{progress.completed} of {progress.total} read">
				<div class="aisle-progress-bar">
					<div class="aisle-progress-fill" style="width: {progressPct}%"></div>
				</div>
				<span class="aisle-progress-text">{progress.completed}/{progress.total}</span>
			</div>
		{/if}
		{#if placeholder}
			<p class="aisle-coming-soon">Coming soon.</p>
		{/if}
	</button>

	{#if expanded && content}
		<div class="aisle-content">
			{@render content()}
		</div>
	{/if}
</section>

<style>
	.aisle {
		border: 1px solid var(--dao-border);
		border-left: 3px solid var(--variant-color);
		background: var(--dao-surface);
		opacity: 0;
		transform: translateY(12px);
		animation: aisle-appear 400ms var(--easing-smooth) forwards;
		animation-delay: var(--stagger-delay, 0ms);
		transition: border-color var(--duration-fast) var(--easing-linear);
	}

	@keyframes aisle-appear {
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.aisle:hover {
		border-color: var(--variant-color);
	}

	.aisle.placeholder {
		opacity: 0.6;
	}

	.aisle.placeholder:hover {
		border-color: var(--dao-border);
	}

	/* --- Toggle Button --- */

	.aisle-toggle {
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

	.aisle.placeholder .aisle-toggle {
		cursor: default;
	}

	.aisle-header {
		display: flex;
		align-items: baseline;
		gap: var(--space-2);
	}

	.aisle-label {
		font-family: var(--font-sans);
		font-size: var(--type-sm);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		color: var(--variant-color);
		margin: 0;
		font-weight: 600;
	}

	.aisle-count {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
		opacity: 0.5;
	}

	.aisle-chevron {
		font-size: var(--type-sm);
		color: var(--dao-muted);
		margin-left: auto;
		transition: transform var(--duration-fast) var(--easing-linear);
	}

	.aisle-tagline {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		line-height: var(--leading-relaxed);
		margin: var(--space-0-5) 0 0 0;
	}

	.aisle-preview {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-text-secondary);
		margin: var(--space-1) 0 0 0;
		letter-spacing: var(--tracking-wide);
	}

	/* --- Mini Progress Bar --- */

	.aisle-progress {
		display: flex;
		align-items: center;
		gap: var(--space-1);
		margin-top: var(--space-1);
	}

	.aisle-progress-bar {
		flex: 1;
		height: 2px;
		background: var(--dao-border-subtle);
		border-radius: 1px;
		overflow: hidden;
		max-width: 120px;
	}

	.aisle-progress-fill {
		height: 100%;
		background: var(--variant-color);
		border-radius: 1px;
		transition: width var(--duration-normal) var(--easing-enter);
	}

	.aisle-progress-text {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
		opacity: 0.5;
	}

	.aisle-coming-soon {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		margin: var(--space-1) 0 0 0;
	}

	/* --- Expanded Content --- */

	.aisle-content {
		border-top: 1px solid var(--dao-border-subtle);
		padding: var(--space-2) var(--space-3) var(--space-3);
	}

	/* --- Reduced Motion --- */

	@media (prefers-reduced-motion: reduce) {
		.aisle {
			opacity: 1;
			transform: none;
			animation: none;
		}

		.aisle-chevron,
		.aisle-progress-fill {
			transition: none;
		}
	}

	/* --- Touch Targets --- */

	@media (pointer: coarse) {
		.aisle-toggle {
			min-height: 44px;
		}
	}
</style>
