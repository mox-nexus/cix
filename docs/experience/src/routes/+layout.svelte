<script lang="ts">
	import '../app.css';
	import { page } from '$app/state';
	import { SiteNav } from '$lib/components/nav';

	let { children } = $props();

	let isLanding = $derived(page.url.pathname === '/');
</script>

<svelte:head>
	<title>cix — Collaborative Intelligence Extensions</title>
	<meta name="description" content="Extensions that enhance human capability, not replace it." />
</svelte:head>

<a href="#main" class="skip-link">Skip to content</a>

{#if !isLanding}
	<SiteNav />
{/if}

<div class="page" class:has-nav={!isLanding}>
	{@render children()}
</div>

<div class="experimental-tag" aria-hidden="true">experimental</div>

<style>
	.has-nav {
		padding-top: var(--header-height, 54px);
	}

	.experimental-tag {
		position: fixed;
		bottom: var(--space-1);
		right: var(--space-1);
		font-family: var(--font-mono);
		font-size: 0.55rem;
		letter-spacing: 0.15em;
		text-transform: uppercase;
		color: var(--dao-muted, #555);
		opacity: 0.4;
		pointer-events: none;
		z-index: 9999;
	}
</style>
