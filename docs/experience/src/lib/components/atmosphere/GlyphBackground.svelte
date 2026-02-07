<script lang="ts">
	import { glyphConfig } from '$lib/stores/glyph';
	import type { Snippet } from 'svelte';

	// Allow prop overrides for direct usage, otherwise use store
	let {
		opacity,
		blur,
		position,
		children
	}: {
		opacity?: number;
		blur?: number;
		position?: string;
		children?: Snippet;
	} = $props();

	// Reactive: use props if provided, otherwise store values
	let config = $derived({
		opacity: opacity ?? $glyphConfig.opacity,
		blur: blur ?? $glyphConfig.blur,
		position: position ?? $glyphConfig.position,
		visible: $glyphConfig.visible
	});
</script>

{#if config.visible}
<div
	class="glyph-background"
	style:--glyph-opacity={config.opacity}
	style:--glyph-blur="{config.blur}px"
	style:--glyph-position={config.position}
	aria-hidden="true"
>
	<div class="glyph-layer glyph-image"></div>
	<div class="glyph-layer glyph-vignette"></div>
</div>
{/if}

{#if children}
	{@render children()}
{/if}

<style>
	.glyph-background {
		position: fixed;
		inset: 0;
		z-index: -1;
		pointer-events: none;
		overflow: hidden;
	}

	.glyph-layer {
		position: absolute;
		inset: 0;
	}

	.glyph-image {
		/* The canonical glyph - blue spark, red containment, void, 4 green structures */
		background-image: url('/sigil.svg');
		background-repeat: no-repeat;
		background-position: var(--glyph-position);
		background-size: min(100vw, 100vh);

		/* Softening treatment - present but atmospheric */
		opacity: var(--glyph-opacity);
		filter: blur(var(--glyph-blur));

		/* Luminous blend with the void */
		mix-blend-mode: lighten;
	}

	.glyph-vignette {
		/* Fade edges into the void - reinforce the darkness */
		background: radial-gradient(
			ellipse 70% 70% at center 40%,
			transparent 20%,
			oklch(10% 0.003 60 / 0.5) 50%,
			oklch(8% 0.002 60) 80%,
			oklch(6% 0.002 60) 100%
		);
	}

	/* Reduced motion: slightly more diffuse */
	@media (prefers-reduced-motion: reduce) {
		.glyph-image {
			filter: blur(calc(var(--glyph-blur) * 1.5));
		}
	}
</style>
