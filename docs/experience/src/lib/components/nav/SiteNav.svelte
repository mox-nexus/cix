<script lang="ts">
	import { page } from '$app/state';

	const links = [
		{ href: '/ethos', label: 'ethos' },
		{ href: '/catalog', label: 'catalog' },
		{ href: '/library', label: 'library' }
	];

	let currentPath = $derived(page.url.pathname);
</script>

<nav class="site-nav" aria-label="Site navigation">
	<a href="/" class="nav-wordmark">cix</a>

	<div class="nav-links">
		{#each links as link}
			<a
				href={link.href}
				class="nav-link"
				class:active={currentPath.startsWith(link.href)}
				aria-current={currentPath.startsWith(link.href) ? 'page' : undefined}
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
