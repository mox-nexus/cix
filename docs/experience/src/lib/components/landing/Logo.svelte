<script lang="ts">
	import { onMount } from 'svelte';

	interface Props {
		maxSize?: string;
	}

	let { maxSize = 'min(28.125vh, 25.3125vw)' }: Props = $props();

	let time = $state(0);
	let reducedMotion = $state(false);

	onMount(() => {
		const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
		reducedMotion = mq.matches;

		if (reducedMotion) return;

		let animId: number;
		let last = performance.now();
		const animate = (now: number) => {
			time += now - last;
			last = now;
			animId = requestAnimationFrame(animate);
		};
		animId = requestAnimationFrame(animate);
		return () => cancelAnimationFrame(animId);
	});

	// Heptagon rotates clockwise
	let heptagonRotation = $derived((time * 0.0072) % 360);
	// Spark rotates counter-clockwise
	let sparkRotation = $derived(-(time * 0.01) % 360);
</script>

<div class="logo" style="--max-size: {maxSize}">
	<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" class="mark">
		<!-- Layer 1: Green d-primitive — all dimensions ×1.333 from reference -->
		<circle cx="100" cy="100" r="21" fill="none" stroke-width="5.13" class="emergence" />
		<line x1="100" y1="79" x2="100" y2="40" stroke-width="5.13" stroke-linecap="round" class="emergence" />

		<!-- Layer 2: Red heptagon (r=60) — slow clockwise rotation -->
		<g transform="rotate({heptagonRotation}, 100, 100)">
			<path d="M 100.00 40.00 L 146.91 62.59 L 158.49 113.35 L 126.03 154.05 L 73.97 154.05 L 41.51 113.35 L 53.09 62.59 Z" fill="none" stroke-width="3.50" stroke-linejoin="round" opacity="0.9" class="heptagon" />
			<path d="M 100.00 40.00 L 158.49 113.35 L 73.97 154.05 L 53.09 62.59 L 146.91 62.59 L 126.03 154.05 L 41.51 113.35 Z" fill="none" stroke-width="1.05" stroke-linejoin="round" opacity="0.2" class="heptagon" />
			<circle cx="100.00" cy="40.00" r="2" opacity="0.5" class="heptagon-dot" />
			<circle cx="146.91" cy="62.59" r="2" opacity="0.5" class="heptagon-dot" />
			<circle cx="158.49" cy="113.35" r="2" opacity="0.5" class="heptagon-dot" />
			<circle cx="126.03" cy="154.05" r="2" opacity="0.5" class="heptagon-dot" />
			<circle cx="73.97" cy="154.05" r="2" opacity="0.5" class="heptagon-dot" />
			<circle cx="41.51" cy="113.35" r="2" opacity="0.5" class="heptagon-dot" />
			<circle cx="53.09" cy="62.59" r="2" opacity="0.5" class="heptagon-dot" />
		</g>

		<!-- Layer 3: Blue spark — 3 rays at 120°, counter-clockwise rotation -->
		<g transform="rotate({sparkRotation}, 100, 100)">
			<line x1="100" y1="100" x2="100" y2="65" stroke-width="5.5" stroke-linecap="round" class="spark" />
			<line x1="100" y1="100" x2="130.31" y2="117.50" stroke-width="5.5" stroke-linecap="round" class="spark" />
			<line x1="100" y1="100" x2="69.69" y2="117.50" stroke-width="5.5" stroke-linecap="round" class="spark" />
			<circle cx="100" cy="100" r="8.75" class="spark-fill" />
		</g>
	</svg>
</div>

<style>
	.logo {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100%;
	}

	.mark {
		width: var(--max-size);
		height: var(--max-size);
		display: block;
	}

	.heptagon {
		stroke: var(--ci-red);
	}

	.heptagon-dot {
		fill: var(--ci-red);
	}

	.emergence {
		stroke: var(--emergence-core);
	}

	.spark {
		stroke: oklch(80% 0.22 245);
	}

	.spark-fill {
		fill: oklch(80% 0.22 245);
	}
</style>
