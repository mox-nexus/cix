<script lang="ts">
	interface Props {
		id: string;
		label: string;
		tagline: string;
		count: number;
		preview?: string;
		progress?: { completed: number; total: number };
		placeholder?: boolean;
		variant?: string;
		delay?: number;
		active?: boolean;
		suggestedSlug?: string;
		suggestedTitle?: string;
		suggestedMeta?: string;
		onclick: () => void;
	}

	let {
		id,
		label,
		tagline,
		count,
		preview,
		progress,
		placeholder = false,
		variant = 'explanation',
		delay = 0,
		active = false,
		suggestedSlug,
		suggestedTitle,
		suggestedMeta,
		onclick
	}: Props = $props();

	import { base } from '$app/paths';

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

<div
	class="quadrant-card"
	class:active
	class:placeholder
	style="--stagger-delay: {delay}ms; --variant-color: {variantColor}"
>
	<button
		class="card-toggle"
		onclick={onclick}
		disabled={placeholder}
		aria-expanded={active}
		aria-controls={id}
	>
		<div class="card-header">
			<h2 class="card-label">{label}</h2>
			<span class="card-count">{count}</span>
		</div>
		<p class="card-tagline">{tagline}</p>
		{#if preview}
			<p class="card-preview">{preview}</p>
		{/if}
		{#if progress && progress.total > 0}
			<div class="card-progress">
				<div class="card-progress-bar">
					<div class="card-progress-fill" style="width: {progressPct}%"></div>
				</div>
				<span class="card-progress-text">{progress.completed}/{progress.total}</span>
			</div>
		{/if}
		{#if placeholder}
			<p class="card-coming-soon">Coming soon.</p>
		{/if}
	</button>

	{#if suggestedSlug && suggestedTitle}
		<a href="{base}/library/explanation/{suggestedSlug}" class="card-suggested">
			<span class="suggested-badge">start here</span>
			<span class="suggested-title">{suggestedTitle}</span>
			{#if suggestedMeta}
				<span class="suggested-meta">{suggestedMeta}</span>
			{/if}
		</a>
	{/if}
</div>

<style>
	.quadrant-card {
		border: 1px solid var(--dao-border);
		border-left: 3px solid var(--variant-color);
		background: var(--dao-surface);
		opacity: 0;
		transform: translateY(12px);
		animation: card-appear 400ms var(--easing-smooth) forwards;
		animation-delay: var(--stagger-delay, 0ms);
		transition: border-color var(--duration-fast) var(--easing-linear);
	}

	.quadrant-card.placeholder {
		--card-final-opacity: 0.5;
	}

	@keyframes card-appear {
		to {
			opacity: var(--card-final-opacity, 1);
			transform: translateY(0);
		}
	}

	.quadrant-card:hover:not(.placeholder) {
		border-color: var(--variant-color);
	}

	.quadrant-card.active {
		border-color: var(--variant-color);
	}

	/* --- Toggle Button --- */

	.card-toggle {
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

	.quadrant-card.placeholder .card-toggle {
		cursor: default;
	}

	.card-header {
		display: flex;
		align-items: baseline;
		gap: var(--space-2);
	}

	.card-label {
		font-family: var(--font-sans);
		font-size: var(--type-xs);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		color: var(--variant-color);
		margin: 0;
		font-weight: 600;
	}

	.card-count {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
		opacity: 0.5;
	}

	.card-tagline {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		line-height: var(--leading-relaxed);
		margin: var(--space-0-5) 0 0 0;
	}

	.card-preview {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-text-secondary);
		margin: var(--space-1) 0 0 0;
		letter-spacing: var(--tracking-wide);
	}

	/* --- Progress Bar --- */

	.card-progress {
		display: flex;
		align-items: center;
		gap: var(--space-1);
		margin-top: var(--space-1-5);
	}

	.card-progress-bar {
		flex: 1;
		height: 2px;
		background: var(--dao-border-subtle);
		border-radius: 1px;
		overflow: hidden;
	}

	.card-progress-fill {
		height: 100%;
		background: var(--variant-color);
		border-radius: 1px;
		transition: width var(--duration-normal) var(--easing-enter);
	}

	.card-progress-text {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
		opacity: 0.5;
	}

	.card-coming-soon {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		margin: var(--space-1) 0 0 0;
	}

	/* --- Suggested Entry --- */

	.card-suggested {
		display: flex;
		align-items: baseline;
		gap: var(--space-1);
		padding: var(--space-1) var(--space-3) var(--space-2);
		border-top: 1px solid var(--dao-border-subtle);
		text-decoration: none;
		transition: background var(--duration-fast) var(--easing-linear);
	}

	.card-suggested:hover {
		background: var(--dao-bg);
	}

	.suggested-badge {
		font-family: var(--font-sans);
		font-size: var(--type-xs);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		color: var(--spark-core);
		white-space: nowrap;
	}

	.suggested-title {
		font-family: var(--font-sans);
		font-size: var(--type-sm);
		font-weight: 600;
		color: var(--dao-text);
	}

	.suggested-meta {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
	}

	/* --- Reduced Motion --- */

	@media (prefers-reduced-motion: reduce) {
		.quadrant-card {
			opacity: 1;
			transform: none;
			animation: none;
		}

		.card-progress-fill {
			transition: none;
		}
	}

	/* --- Touch Targets --- */

	@media (pointer: coarse) {
		.card-toggle {
			min-height: 44px;
		}
	}
</style>
