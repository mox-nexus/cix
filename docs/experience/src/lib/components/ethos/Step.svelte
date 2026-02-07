<script lang="ts">
	import { getContext } from 'svelte';
	import type { Snippet } from 'svelte';

	let {
		children,
		stat
	}: {
		children: Snippet;
		stat?: { value: number; label: string; source?: string };
	} = $props();

	const scene = getContext<{ progress: number; isActive: boolean; id: string }>('scene');

	let element: HTMLDivElement;
	let isVisible = $state(false);

	// Intersection observer for visibility
	$effect(() => {
		if (!element) return;

		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					isVisible = entry.isIntersecting;
				});
			},
			{ threshold: 0.5, rootMargin: '-20% 0px -20% 0px' }
		);

		observer.observe(element);
		return () => observer.disconnect();
	});
</script>

<div class="step" class:visible={isVisible} bind:this={element}>
	<div class="step-content">
		{@render children()}
	</div>

	{#if stat}
		<div class="step-stat">
			<span class="stat-value">{stat.value}%</span>
			<span class="stat-label">{stat.label}</span>
			{#if stat.source}
				<cite class="stat-source">{stat.source}</cite>
			{/if}
		</div>
	{/if}
</div>

<style>
	.step {
		min-height: 50vh;
		display: flex;
		flex-direction: column;
		justify-content: center;
		padding: var(--space-4) 0;
		opacity: 0.3;
		transition: opacity var(--duration-slow) var(--easing-linear);
	}

	.step.visible {
		opacity: 1;
	}

	.step-content {
		font-size: var(--type-base);
		line-height: var(--leading-snug);
	}

	.step-content :global(p) {
		margin-block: var(--space-2);
	}

	.step-stat {
		margin-top: var(--space-3);
		padding: var(--space-2);
		background: var(--dao-surface);
		border-left: var(--border-accent) solid var(--dao-green);
		border-radius: var(--radius-sm);
	}

	.stat-value {
		display: block;
		font-family: var(--font-sans);
		font-size: var(--type-xl);
		font-weight: 600;
		color: var(--dao-green);
		line-height: 1;
	}

	.stat-label {
		display: block;
		font-size: var(--type-sm);
		color: var(--dao-muted);
		margin-top: var(--space-1);
	}

	.stat-source {
		display: block;
		font-size: var(--type-sm);
		color: var(--spark-core);
		margin-top: var(--space-1);
		font-style: normal;
	}

	.stat-source::before {
		content: '— ';
	}

	/* Reduced motion */
	@media (prefers-reduced-motion: reduce) {
		.step {
			opacity: 1;
			transition: none;
		}
	}
</style>
