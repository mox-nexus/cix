<script lang="ts">
	import { onMount } from 'svelte';

	let isVisible = $state(false);
	let phase = $state(0); // 0: hidden, 1: rings appear, 2: labels appear
	let element: HTMLDivElement;

	onMount(() => {
		const observer = new IntersectionObserver(
			(entries) => {
				if (entries[0].isIntersecting && !isVisible) {
					isVisible = true;
					// Staggered reveal
					setTimeout(() => phase = 1, 200);
					setTimeout(() => phase = 2, 800);
				}
			},
			{ threshold: 0.3 }
		);

		observer.observe(element);
		return () => observer.disconnect();
	});
</script>

<div class="extended-mind" bind:this={element} class:visible={isVisible}>
	<svg viewBox="0 0 400 400" class="mind-diagram" aria-label="Extended mind diagram">
		<!-- Outermost ring (environment) -->
		<circle
			cx="200" cy="200" r="180"
			class="ring ring-outer"
			class:animate={phase >= 1}
			style="--delay: 400ms"
		/>
		<text
			x="200" y="35"
			class="ring-label"
			class:show={phase >= 2}
			style="--delay: 200ms"
		>Environment</text>

		<!-- Middle ring (tools, notebooks) -->
		<circle
			cx="200" cy="200" r="120"
			class="ring ring-middle"
			class:animate={phase >= 1}
			style="--delay: 200ms"
		/>
		<text
			x="200" y="95"
			class="ring-label"
			class:show={phase >= 2}
			style="--delay: 100ms"
		>Tools, Notes</text>

		<!-- Inner ring (working memory) -->
		<circle
			cx="200" cy="200" r="60"
			class="ring ring-inner"
			class:animate={phase >= 1}
			style="--delay: 0ms"
		/>

		<!-- Core (you) -->
		<circle
			cx="200" cy="200" r="24"
			class="core"
			class:animate={phase >= 1}
		/>
		<text
			x="200" y="206"
			class="core-label"
			class:show={phase >= 2}
		>You</text>

		<!-- Otto's notebook (positioned in the middle ring) -->
		<g class="notebook" class:show={phase >= 2} transform="translate(280, 180)">
			<rect
				x="0" y="0"
				width="50" height="65"
				rx="2"
				class="notebook-cover"
			/>
			<line x1="8" y1="18" x2="42" y2="18" class="notebook-line" />
			<line x1="8" y1="28" x2="42" y2="28" class="notebook-line" />
			<line x1="8" y1="38" x2="35" y2="38" class="notebook-line" />
			<text x="25" y="58" class="notebook-label">Otto's</text>
		</g>
	</svg>

	<p class="mind-caption" class:show={phase >= 2}>
		"If the notebook performs the same cognitive function as memory,
		it's part of the cognitive system."
		<cite>— Clark & Chalmers, 1998</cite>
	</p>
</div>

<style>
	.extended-mind {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: var(--space-3);
		padding: var(--space-4);
	}

	.mind-diagram {
		width: 100%;
		max-width: 400px;
		height: auto;
	}

	/* Rings */
	.ring {
		fill: none;
		stroke-width: 2;
		opacity: 0;
		transform-origin: center;
		transform: scale(0.8);
		transition: all 600ms var(--easing-smooth);
		transition-delay: var(--delay, 0ms);
	}

	.ring.animate {
		opacity: 1;
		transform: scale(1);
	}

	.ring-outer {
		stroke: var(--spark-atmosphere);
		stroke-dasharray: 8 4;
	}

	.ring-middle {
		stroke: var(--spark-outer);
	}

	.ring-inner {
		stroke: var(--spark-inner);
		stroke-width: 3;
	}

	/* Core */
	.core {
		fill: var(--spark-core);
		opacity: 0;
		transform-origin: center;
		transform: scale(0);
		transition: all 400ms var(--easing-smooth);
	}

	.core.animate {
		opacity: 1;
		transform: scale(1);
	}

	/* Labels */
	.ring-label,
	.core-label {
		font-family: var(--font-mono);
		font-size: 12px;
		fill: var(--dao-muted);
		text-anchor: middle;
		opacity: 0;
		transition: opacity 400ms var(--easing-smooth);
		transition-delay: var(--delay, 0ms);
	}

	.ring-label.show,
	.core-label.show {
		opacity: 1;
	}

	.core-label {
		fill: var(--dao-bg);
		font-weight: 600;
	}

	/* Otto's Notebook */
	.notebook {
		opacity: 0;
		transform: translateX(10px);
		transition: all 500ms var(--easing-smooth) 400ms;
	}

	.notebook.show {
		opacity: 1;
		transform: translateX(0) rotate(-2deg);
	}

	.notebook-cover {
		fill: var(--dao-surface);
		stroke: var(--spark-outer);
		stroke-width: 1;
	}

	.notebook-line {
		stroke: var(--dao-muted);
		stroke-width: 1;
		opacity: 0.4;
	}

	.notebook-label {
		font-family: var(--font-mono);
		font-size: 10px;
		fill: var(--dao-muted);
		text-anchor: middle;
	}

	/* Caption */
	.mind-caption {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-text-secondary);
		text-align: center;
		max-width: 400px;
		line-height: var(--leading-relaxed);
		opacity: 0;
		transform: translateY(10px);
		transition: all 500ms var(--easing-smooth) 600ms;
	}

	.mind-caption.show {
		opacity: 1;
		transform: translateY(0);
	}

	.mind-caption cite {
		display: block;
		font-size: var(--type-xs);
		color: var(--spark-core);
		margin-top: var(--space-1);
		font-style: normal;
	}

	@media (prefers-reduced-motion: reduce) {
		.ring,
		.core,
		.notebook,
		.mind-caption,
		.ring-label,
		.core-label {
			opacity: 1;
			transform: none;
			transition: none;
		}
	}
</style>
