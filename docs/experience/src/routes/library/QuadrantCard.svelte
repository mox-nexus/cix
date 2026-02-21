<script lang="ts">
	import { base } from '$app/paths';

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
		delay = 0
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
	let href = $derived(placeholder ? undefined : `${base}/library/${id}`);
</script>

{#if placeholder}
	<div
		class="quadrant-card placeholder"
		style="--stagger-delay: {delay}ms; --variant-color: {variantColor}"
	>
		<div class="card-body">
			<div class="card-header">
				<h2 class="card-label">{label}</h2>
			</div>
			<p class="card-tagline">{tagline}</p>
			<p class="card-coming-soon">Coming soon.</p>
		</div>
	</div>
{:else}
	<a
		{href}
		class="quadrant-card"
		style="--stagger-delay: {delay}ms; --variant-color: {variantColor}"
	>
		<div class="card-body">
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
		</div>
		<span class="card-arrow" aria-hidden="true">&rarr;</span>
	</a>
{/if}

<style>
	.quadrant-card {
		display: flex;
		align-items: center;
		border: 1px solid var(--dao-border);
		border-left: 3px solid var(--variant-color);
		background: transparent;
		text-decoration: none;
		color: inherit;
		opacity: 0;
		transform: translateY(12px);
		animation: card-appear 400ms var(--easing-smooth) forwards;
		animation-delay: var(--stagger-delay, 0ms);
		transition: border-color var(--duration-fast) var(--easing-linear);
	}

	.quadrant-card.placeholder {
		--card-final-opacity: 1;
	}

	.quadrant-card.placeholder .card-label {
		color: var(--dao-muted);
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

	.card-body {
		flex: 1;
		padding: var(--space-3) var(--space-3);
	}

	.card-header {
		display: flex;
		align-items: baseline;
		gap: var(--space-2);
	}

	.card-label {
		font-family: var(--font-sans);
		font-size: var(--type-lg);
		color: var(--variant-color);
		margin: 0;
		font-weight: 600;
	}

	.card-count {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
	}

	.card-tagline {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		line-height: var(--leading-relaxed);
		margin: var(--space-1) 0 0 0;
	}

	.card-preview {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-text-secondary);
		margin: var(--space-1) 0 0 0;
		letter-spacing: var(--tracking-wide);
	}

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
	}

	.card-coming-soon {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		margin: var(--space-1) 0 0 0;
	}

	.card-arrow {
		font-size: var(--type-xl);
		color: var(--dao-muted);
		padding-right: var(--space-3);
		transition: color var(--duration-fast) var(--easing-linear);
	}

	.quadrant-card:hover .card-arrow {
		color: var(--variant-color);
	}

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

	@media (pointer: coarse) {
		.card-body {
			min-height: 44px;
		}
	}
</style>
