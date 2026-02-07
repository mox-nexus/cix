<script lang="ts">
	import { onMount } from 'svelte';

	interface Props {
		maxSize?: string;
	}

	let { maxSize = '180px' }: Props = $props();

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

	let heptagonRotation = $derived((time * 0.0072) % 360);
	let sparkRotation = $derived(-(time * 0.01) % 360);
	let morphProgress = $derived((Math.sin(time * 0.001) + 1) / 2);

	// Staggered: arm2 appears in first half, arm3 in second half → 1→2→3→2→1
	let arm2Progress = $derived(Math.min(1, morphProgress * 2));
	let arm3Progress = $derived(Math.max(0, (morphProgress - 0.5) * 2));
</script>

<div class="logo" style="--max-size: {maxSize}">
	<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" class="mark">
		<!-- Layer 1: Red heptagon — slow clockwise rotation -->
		<g transform="rotate({heptagonRotation}, 100, 100)">
			<path d="M 100.00 55.00 L 135.18 71.94 L 143.87 110.01 L 119.52 140.54 L 80.48 140.54 L 56.13 110.01 L 64.82 71.94 Z" fill="none" stroke-width="3.50" stroke-linejoin="round" opacity="0.9" class="heptagon" />
			<path d="M 100.00 55.00 L 143.87 110.01 L 80.48 140.54 L 64.82 71.94 L 135.18 71.94 L 119.52 140.54 L 56.13 110.01 Z" fill="none" stroke-width="1.05" stroke-linejoin="round" opacity="0.2" class="heptagon" />
			<circle cx="100.00" cy="55.00" r="1.75" opacity="0.5" class="heptagon-dot" />
			<circle cx="135.18" cy="71.94" r="1.75" opacity="0.5" class="heptagon-dot" />
			<circle cx="143.87" cy="110.01" r="1.75" opacity="0.5" class="heptagon-dot" />
			<circle cx="119.52" cy="140.54" r="1.75" opacity="0.5" class="heptagon-dot" />
			<circle cx="80.48" cy="140.54" r="1.75" opacity="0.5" class="heptagon-dot" />
			<circle cx="56.13" cy="110.01" r="1.75" opacity="0.5" class="heptagon-dot" />
			<circle cx="64.82" cy="71.94" r="1.75" opacity="0.5" class="heptagon-dot" />
		</g>

		<!-- Layer 2: Green emergence — triskelion morph -->
		<circle cx="100" cy="100" r="15.75" fill="none" stroke-width="3.85" class="emergence" />
		<!-- Arm 1: up (-90°) — always visible -->
		<line x1="100" y1="84.25" x2="100" y2="55" stroke-width="3.85" stroke-linecap="round" class="emergence" />
		<!-- Arm 2: lower-right (30°) — appears first -->
		<line x1="113.64" y1="107.88" x2="138.97" y2="122.5"
			stroke-width={3.85 * arm2Progress} stroke-linecap="round" class="emergence"
			opacity={arm2Progress} />
		<!-- Arm 3: lower-left (150°) — appears second -->
		<line x1="86.36" y1="107.88" x2="61.03" y2="122.5"
			stroke-width={3.85 * arm3Progress} stroke-linecap="round" class="emergence"
			opacity={arm3Progress} />
		<!-- Center dot — appears during triskelion phase -->
		<circle cx="100" cy="100" r="1.5" class="emergence-fill" opacity={0.3 * arm3Progress} />

		<!-- Layer 3: Blue spark — slow counter-clockwise rotation -->
		<g transform="rotate({sparkRotation}, 100, 100)">
			<line x1="100" y1="100" x2="119.49" y2="88.75" stroke-width="4.00" stroke-linecap="round" class="spark" />
			<line x1="100" y1="100" x2="100.00" y2="122.50" stroke-width="4.00" stroke-linecap="round" class="spark" />
			<line x1="100" y1="100" x2="80.51" y2="88.75" stroke-width="4.00" stroke-linecap="round" class="spark" />
			<circle cx="100" cy="100" r="6.50" class="spark-fill" />
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
		width: 100%;
		height: 100%;
		max-width: var(--max-size);
		max-height: var(--max-size);
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

	.emergence-fill {
		fill: var(--emergence-core);
	}

	.spark {
		stroke: var(--spark-core);
	}

	.spark-fill {
		fill: var(--spark-core);
	}
</style>
