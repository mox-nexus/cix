<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		north?: Snippet;
		west?: Snippet;
		center?: Snippet;
		east?: Snippet;
		south?: Snippet;
		marginSW?: Snippet;
		marginSE?: Snippet;
	}

	let {
		north,
		west,
		center,
		east,
		south,
		marginSW,
		marginSE
	}: Props = $props();
</script>

<div class="landing-grid">
	<!-- Atmospheric gradient -->
	<div class="atmosphere" aria-hidden="true"></div>

	<!-- Cardinal positions -->
	<header class="pos-north">
		{#if north}{@render north()}{/if}
	</header>

	<aside class="pos-west">
		{#if west}{@render west()}{/if}
	</aside>

	<main class="pos-center">
		{#if center}{@render center()}{/if}
	</main>

	<aside class="pos-east">
		{#if east}{@render east()}{/if}
	</aside>

	<nav class="pos-south">
		{#if south}{@render south()}{/if}
	</nav>

	<!-- Margin positions -->
	<footer class="pos-margin-sw">
		{#if marginSW}{@render marginSW()}{/if}
	</footer>

	<div class="pos-margin-se">
		{#if marginSE}{@render marginSE()}{/if}
	</div>
</div>

<style>
	.landing-grid {
		height: 100vh;
		height: 100dvh;
		position: relative;
		overflow: hidden;

		display: grid;
		/*
		 * Columns: sidebars get min-content, center expands
		 * Rows: north/south get auto (min needed), center row expands
		 */
		grid-template-columns: minmax(min-content, 1fr) minmax(180px, 1.2fr) minmax(min-content, 1fr);
		grid-template-rows: auto 1fr auto;
		grid-template-areas:
			".         north      ."
			"west      center     east"
			"margin-sw south      margin-se";
		gap: var(--space-2);
		padding: var(--space-3);
	}

	.atmosphere {
		position: absolute;
		inset: 0;
		pointer-events: none;
		z-index: 0;
		background:
			radial-gradient(
				ellipse 60% 50% at 15% 15%,
				var(--spark-atmosphere) 0%,
				transparent 65%
			),
			radial-gradient(
				ellipse 80% 60% at 50% 110%,
				var(--emergence-atmosphere) 0%,
				transparent 55%
			);
	}

	/* Cardinal positions */
	.pos-north {
		grid-area: north;
		z-index: 1;
		align-self: end;
	}

	.pos-west {
		grid-area: west;
		z-index: 1;
		display: flex;
		align-items: center;
		justify-content: flex-start;
		padding-left: var(--space-3);
	}

	.pos-center {
		grid-area: center;
		z-index: 1;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.pos-east {
		grid-area: east;
		z-index: 1;
		display: flex;
		align-items: center;
		padding-left: var(--space-2);
	}

	.pos-south {
		grid-area: south;
		z-index: 1;
		align-self: start;
	}

	/* Margin positions */
	.pos-margin-sw {
		grid-area: margin-sw;
		z-index: 1;
		align-self: center;
	}

	.pos-margin-se {
		grid-area: margin-se;
		z-index: 1;
		align-self: end;
		justify-self: end;
	}

	/* Tablet */
	@media (max-width: 1024px) {
		.landing-grid {
			grid-template-columns: 1fr 2fr 1fr;
			padding: var(--space-3);
		}
	}

	/* Mobile: Scrollytelling - vertical stack of components */
	@media (max-width: 768px) {
		.landing-grid {
			display: flex;
			flex-direction: column;
			gap: 0;
			padding: 0;
			min-height: auto;
		}

		/* Control the scroll order */
		.pos-north { order: 1; }
		.pos-center { order: 2; }
		.pos-south { order: 3; }
		.pos-west { order: 4; }
		.pos-east { order: 5; }
		.pos-margin-sw { order: 6; }
		.pos-margin-se { order: 7; }

		/* Each section becomes a full-viewport "slide" */
		.pos-north,
		.pos-center,
		.pos-south,
		.pos-west,
		.pos-east,
		.pos-margin-sw,
		.pos-margin-se {
			min-height: 100vh;
			min-height: 100dvh;
			display: flex;
			flex-direction: column;
			align-items: center;
			justify-content: center;
			padding: var(--space-4);
		}

		/* Smaller sections don't need full viewport */
		.pos-south,
		.pos-margin-sw,
		.pos-margin-se {
			min-height: 50vh;
			min-height: 50dvh;
		}

		/* Hide empty margin */
		.pos-margin-se:empty {
			display: none;
			min-height: 0;
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.atmosphere {
			background: none;
		}
	}
</style>
