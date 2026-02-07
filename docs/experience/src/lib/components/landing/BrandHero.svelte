<script lang="ts">
	interface Props {
		brand?: string;
		tagline?: string;
	}

	let {
		brand = 'cix',
		tagline = 'marketplace for extensions that enhance AI collaboration'
	}: Props = $props();
</script>

<header class="brand-hero">
	<h1 class="brand">{brand}</h1>
	<p class="tagline">{tagline}</p>
</header>

<style>
	.brand-hero {
		text-align: center;
	}

	.brand {
		font-family: var(--font-sans);
		font-size: var(--type-4xl);
		font-weight: 700;
		letter-spacing: var(--tracking-tight);
		margin: 0;
		color: var(--spark-core);
		text-shadow:
			0 0 4px oklch(75% 0.18 240),
			0 0 12px oklch(62% 0.15 240 / 0.6),
			0 0 30px oklch(55% 0.12 240 / 0.3),
			0 0 60px oklch(50% 0.08 240 / 0.1);
	}

	.tagline {
		font-family: var(--font-mono);
		font-size: var(--type-base);
		color: var(--dao-text-secondary);
		letter-spacing: var(--tracking-wide);
		margin: var(--space-1) 0 0;
	}

	@media (prefers-reduced-motion: reduce) {
		.brand {
			text-shadow: none;
		}
	}
</style>
