<script lang="ts">
	import { onMount } from 'svelte';

	interface Props {
		leftValue: number;
		leftLabel: string;
		rightValue: number;
		rightLabel: string;
		unit?: string;
	}

	let {
		leftValue,
		leftLabel,
		rightValue,
		rightLabel,
		unit = '%'
	}: Props = $props();

	let leftDisplay = $state(0);
	let rightDisplay = $state(0);
	let isVisible = $state(false);
	let element: HTMLDivElement;

	onMount(() => {
		const observer = new IntersectionObserver(
			(entries) => {
				if (entries[0].isIntersecting && !isVisible) {
					isVisible = true;
					animateCounters();
				}
			},
			{ threshold: 0.5 }
		);

		observer.observe(element);
		return () => observer.disconnect();
	});

	function animateCounters() {
		const duration = 1200;
		const startTime = performance.now();

		function tick(currentTime: number) {
			const elapsed = currentTime - startTime;
			const progress = Math.min(elapsed / duration, 1);

			// Ease out cubic
			const eased = 1 - Math.pow(1 - progress, 3);

			// Left counts faster (optimism)
			leftDisplay = Math.round(leftValue * Math.min(eased * 1.2, 1));
			// Right counts slower (reality catching up)
			rightDisplay = Math.round(rightValue * eased);

			if (progress < 1) {
				requestAnimationFrame(tick);
			} else {
				leftDisplay = leftValue;
				rightDisplay = rightValue;
			}
		}

		requestAnimationFrame(tick);
	}
</script>

<div class="dueling-stats" bind:this={element} class:visible={isVisible}>
	<div class="stat stat-left">
		<span class="stat-value">{leftDisplay}{unit}</span>
		<span class="stat-label">{leftLabel}</span>
	</div>

	<div class="stat-gap">
		<span class="gap-line"></span>
	</div>

	<div class="stat stat-right">
		<span class="stat-value">{rightDisplay}{unit}</span>
		<span class="stat-label">{rightLabel}</span>
	</div>
</div>

<style>
	.dueling-stats {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: var(--space-4);
		padding: var(--space-4) 0;
	}

	.stat {
		display: flex;
		flex-direction: column;
		align-items: center;
		opacity: 0;
		transform: translateY(20px);
		transition: all 600ms var(--easing-smooth);
	}

	.visible .stat-left {
		opacity: 1;
		transform: translateY(0) translateX(0);
		transition-delay: 0ms;
	}

	.visible .stat-right {
		opacity: 1;
		transform: translateY(0) translateX(0);
		transition-delay: 200ms;
	}

	.stat-value {
		font-family: var(--font-sans);
		font-size: clamp(3rem, 8vw, 4.5rem);
		font-weight: 700;
		line-height: 1;
	}

	.stat-left .stat-value {
		color: var(--spark-core);
		text-shadow:
			0 0 20px oklch(62% 0.15 240 / 0.4),
			0 0 40px oklch(55% 0.12 240 / 0.2);
	}

	.stat-right .stat-value {
		color: var(--ci-red);
		text-shadow:
			0 0 20px oklch(58% 0.18 25 / 0.4),
			0 0 40px oklch(50% 0.15 25 / 0.2);
	}

	.stat-label {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		color: var(--dao-muted);
		margin-top: var(--space-1);
	}

	.stat-gap {
		display: flex;
		align-items: center;
		padding: 0 var(--space-2);
	}

	.gap-line {
		width: 60px;
		height: 2px;
		background: linear-gradient(
			to right,
			var(--spark-core),
			var(--dao-muted) 50%,
			var(--ci-red)
		);
		opacity: 0;
		transform: scaleX(0);
		transition: all 400ms var(--easing-smooth) 600ms;
	}

	.visible .gap-line {
		opacity: 0.6;
		transform: scaleX(1);
	}

	@media (max-width: 640px) {
		.dueling-stats {
			flex-direction: column;
			gap: var(--space-3);
		}

		.stat-gap {
			transform: rotate(90deg);
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.stat {
			opacity: 1;
			transform: none;
			transition: none;
		}

		.gap-line {
			opacity: 0.6;
			transform: scaleX(1);
			transition: none;
		}
	}
</style>
