<script lang="ts">
	import { page } from '$app/state';
	import { base } from '$app/paths';

	const links = [
		{ path: '/catalog', label: 'catalog' },
		{ path: '/library', label: 'library' }
	];

	let currentPath = $derived(page.url.pathname.slice(base.length) || '/');
</script>

<nav class="site-nav" aria-label="Site navigation">
	<a href="{base}/" class="nav-wordmark">cix</a>

	<div class="nav-links">
		{#each links as link}
			<a
				href="{base}{link.path}"
				class="nav-link"
				class:active={currentPath.startsWith(link.path)}
				aria-current={currentPath.startsWith(link.path) ? 'page' : undefined}
			>
				{link.label}
			</a>
		{/each}
	</div>
</nav>

<style>
	.site-nav {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		height: var(--header-height, 54px);
		z-index: var(--z-sticky, 200);

		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0 var(--space-3);

		background: var(--dao-bg);
		border-bottom: 1px solid var(--dao-border);
	}

	.nav-wordmark {
		font-family: var(--font-sans);
		font-size: var(--type-base);
		font-weight: 700;
		color: var(--dao-text);
		text-decoration: none;
		letter-spacing: 0.05em;
		transition: color var(--duration-fast) var(--easing-linear);
	}

	.nav-wordmark:hover {
		color: var(--spark-core);
	}

	.nav-links {
		display: flex;
		gap: var(--space-3);
	}

	.nav-link {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		text-decoration: none;
		padding-bottom: 2px;
		border-bottom: 2px solid transparent;
		transition:
			color var(--duration-fast) var(--easing-linear),
			border-color var(--duration-fast) var(--easing-linear);
	}

	.nav-link:hover {
		color: var(--dao-text);
	}

	.nav-link.active {
		color: var(--spark-core);
		border-bottom-color: var(--spark-core);
	}
</style>
