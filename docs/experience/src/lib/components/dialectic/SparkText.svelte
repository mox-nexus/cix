<script lang="ts">
	import type { Snippet } from 'svelte';

	let {
		as = 'span',
		intensity = 'normal',
		children
	}: {
		as?: 'span' | 'strong' | 'em';
		intensity?: 'subtle' | 'normal' | 'bright';
		children: Snippet;
	} = $props();
</script>

<svelte:element
	this={as}
	class="spark-text"
	class:subtle={intensity === 'subtle'}
	class:normal={intensity === 'normal'}
	class:bright={intensity === 'bright'}
>
	{@render children()}
</svelte:element>

<style>
	.spark-text {
		color: var(--spark-core);
		text-shadow:
			0 0 2px var(--spark-inner),
			0 0 8px var(--spark-outer),
			0 0 20px var(--spark-atmosphere);
	}

	/* 4-layer luminosity system */
	.subtle {
		--spark-core: oklch(70% 0.15 240);
		--spark-inner: oklch(60% 0.12 240 / 0.4);
		--spark-outer: oklch(52% 0.10 240 / 0.15);
		--spark-atmosphere: oklch(48% 0.08 240 / 0.03);
	}

	.normal {
		--spark-core: oklch(75% 0.18 240);
		--spark-inner: oklch(62% 0.15 240 / 0.6);
		--spark-outer: oklch(55% 0.12 240 / 0.2);
		--spark-atmosphere: oklch(50% 0.08 240 / 0.05);
	}

	.bright {
		--spark-core: oklch(82% 0.20 240);
		--spark-inner: oklch(68% 0.17 240 / 0.8);
		--spark-outer: oklch(60% 0.14 240 / 0.3);
		--spark-atmosphere: oklch(55% 0.10 240 / 0.08);
	}

	/* Reduced motion: remove glow, keep color */
	@media (prefers-reduced-motion: reduce) {
		.spark-text {
			text-shadow: none;
			color: var(--dao-blue);
		}
	}
</style>
