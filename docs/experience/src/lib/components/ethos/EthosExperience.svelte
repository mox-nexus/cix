<script lang="ts">
	import { onMount } from 'svelte';
	import { base } from '$app/paths';
	import { scrollToBeat, smoothstep, type BeatState } from './beats';
	import { BEATS as BEAT_CONTENT } from './content';

	interface Props {
		scrollY: number;
	}

	let { scrollY }: Props = $props();

	// Viewport state
	let vh = $state(0);
	let reducedMotion = $state(false);

	let beatState: BeatState = $derived(scrollToBeat(scrollY, vh || 1));

	// Per-beat content opacity with beat-specific fade timing.
	// Each beat breathes differently — the pacing is the design.
	function beatOpacity(targetBeat: number): number {
		const { beat, t } = beatState;
		if (beat !== targetBeat) return 0;

		switch (targetBeat) {
			case 1:
				// Opens visible, holds long, late fade-out
				if (t > 0.8) return 1 - smoothstep((t - 0.8) / 0.2);
				return 1;
			case 2:
				// Fast snap-in (punchy), holds longer — let the shift complete
				if (t < 0.15) return smoothstep(t / 0.15);
				if (t > 0.85) return 1 - smoothstep((t - 0.85) / 0.15);
				return 1;
			case 3:
				// Slower reveal (building), extra hold time
				if (t < 0.25) return smoothstep(t / 0.25);
				if (t > 0.8) return 1 - smoothstep((t - 0.8) / 0.2);
				return 1;
			case 4:
				// Standard reveal, late fade (duty holds weight)
				if (t < 0.2) return smoothstep(t / 0.2);
				if (t > 0.85) return 1 - smoothstep((t - 0.85) / 0.15);
				return 1;
			case 5:
				// Slow reveal, never fades — the invitation stays
				if (t < 0.3) return smoothstep(t / 0.3);
				return 1;
			default:
				return 0;
		}
	}

	// Beat 3 line stagger — each line delays by 0.10 of t.
	// The landing IS the acceleration.
	function lineBeatOpacity(beatId: number, lineIndex: number): number {
		const { beat, t } = beatState;
		if (beat !== beatId) return 0;

		// Only Beat 3 staggers
		if (beatId !== 3) return beatOpacity(beatId);

		const delay = lineIndex * 0.10;
		const effectiveT = Math.max(0, t - delay);

		// Fade in staggered, fade out together
		if (t > 0.8) return 1 - smoothstep((t - 0.8) / 0.2);
		if (effectiveT < 0.25) return smoothstep(effectiveT / 0.25);
		return 1;
	}

	let beat1Opacity = $derived(beatOpacity(1));
	let beat2Opacity = $derived(beatOpacity(2));
	let beat3Opacity = $derived(beatOpacity(3));
	let beat4Opacity = $derived(beatOpacity(4));
	let beat5Opacity = $derived(beatOpacity(5));

	const opacities = $derived([beat1Opacity, beat2Opacity, beat3Opacity, beat4Opacity, beat5Opacity]);

	onMount(() => {
		vh = window.innerHeight;
		reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

		const handleResize = () => {
			vh = window.innerHeight;
		};
		window.addEventListener('resize', handleResize);

		return () => {
			window.removeEventListener('resize', handleResize);
		};
	});

	// Size class mapping
	const SIZE_MAP: Record<string, string> = {
		display: 'var(--type-4xl)',
		hero: 'var(--type-3xl)',
		heading: 'var(--type-2xl)',
		body: 'var(--type-base)',
		small: 'var(--type-sm)'
	};

	const ACCENT_MAP: Record<string, string> = {
		spark: 'var(--spark-core)',
		constraint: 'var(--ci-red)',
		emergence: 'var(--emergence-core)',
		muted: 'var(--dao-text-secondary)'
	};
</script>

<div class="ethos-visual">
	<!-- Content layer -->
	<div class="content-layer" class:reduced-motion={reducedMotion}>
		{#each BEAT_CONTENT as beat, i}
			{@const isBeat3 = beat.id === 3}
			<div
				class="beat-content"
				style="opacity: {reducedMotion ? 1 : isBeat3 ? (opacities[i] > 0 ? 1 : 0) : opacities[i]};
					   pointer-events: {opacities[i] > 0.1 || reducedMotion ? 'auto' : 'none'}"
				class:active={reducedMotion || opacities[i] > 0}
			>
				{#each beat.lines as line, j}
					<p
						class="beat-line"
						style="
							font-family: var(--font-{line.font});
							font-size: {SIZE_MAP[line.size]};
							font-weight: {line.weight ?? 400};
							color: {line.accent ? ACCENT_MAP[line.accent] : 'var(--dao-text)'};
							{line.spacing ? `margin-top: ${line.spacing};` : ''}
							{isBeat3 && !reducedMotion ? `opacity: ${lineBeatOpacity(3, j)};` : ''}
						"
					>
						{line.text}
					</p>
				{/each}

				<!-- Beat 5: cix link at the end -->
				{#if beat.id === 5}
					<a href="{base}/catalog" class="cix-link" style="margin-top: var(--space-3)">
						cix <span class="arrow">&rarr;</span>
					</a>
				{/if}
			</div>
		{/each}
	</div>

	<!-- Back to home wordmark -->
	<a href="{base}/" class="home-wordmark">cix</a>
</div>

<style>
	.ethos-visual {
		position: fixed;
		inset: 0;
		width: 100vw;
		height: 100vh;
		height: 100dvh;
		z-index: 0;
	}

	.content-layer {
		position: absolute;
		inset: 0;
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1;
		pointer-events: none;
	}

	/* Reduced motion: stack all beats vertically */
	.content-layer.reduced-motion {
		position: relative;
		flex-direction: column;
		gap: var(--space-4);
		padding: var(--space-4);
		overflow-y: auto;
		align-items: flex-start;
	}

	.beat-content {
		position: absolute;
		max-width: 72ch;
		padding: 0 var(--space-3);
		text-align: center;
	}

	.reduced-motion .beat-content {
		position: relative;
		text-align: left;
	}

	.beat-line {
		margin: 0;
		line-height: var(--leading-tight, 1.3);
	}

	.cix-link {
		display: inline-flex;
		align-items: baseline;
		gap: 0.5ch;
		font-family: var(--font-sans);
		font-size: var(--type-2xl);
		font-weight: 700;
		color: var(--dao-text);
		text-decoration: none;
		transition: color var(--duration-fast) var(--easing-linear);
	}

	.cix-link:hover {
		color: var(--spark-core);
	}

	.cix-link .arrow {
		transition: transform var(--duration-fast) var(--easing-linear);
		display: inline-block;
		color: var(--spark-core);
	}

	.cix-link:hover .arrow {
		transform: translateX(0.3ch);
	}

	.home-wordmark {
		position: fixed;
		top: var(--space-2);
		left: var(--space-3);
		font-family: var(--font-sans);
		font-size: var(--type-sm);
		font-weight: 700;
		color: var(--dao-muted);
		text-decoration: none;
		z-index: 10;
		opacity: 0.5;
		transition: opacity var(--duration-fast) var(--easing-linear);
	}

	.home-wordmark:hover {
		opacity: 1;
		color: var(--spark-core);
	}

	@media (max-width: 768px) {
		.beat-content {
			padding: 0 var(--space-2);
			max-width: 100%;
		}

		.beat-line {
			word-break: break-word;
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.cix-link,
		.cix-link .arrow,
		.home-wordmark {
			transition: none;
		}
	}
</style>
