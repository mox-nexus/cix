<script lang="ts">
	import { page } from '$app/state';

	const allLinks = [
		{ href: '/ethos', label: 'ethos', description: 'understand why', variant: 'spark' as const },
		{ href: '/catalog', label: 'catalog', description: 'explore extensions', variant: 'emergence' as const },
		{ href: '/library', label: 'library', description: 'deep research', variant: 'constraint' as const }
	];

	let links = $derived(allLinks.filter((l) => !page.url.pathname.startsWith(l.href)));
</script>

<nav class="cross-links" aria-label="Explore other sections">
	<span class="cross-links-label">explore</span>
	<div class="cross-links-list">
		{#each links as link}
			<a href={link.href} class="cross-link cross-link-{link.variant}">
				<span class="link-label">{link.label}</span>
				<span class="link-arrow">&rarr;</span>
				<span class="link-description">{link.description}</span>
			</a>
		{/each}
	</div>
</nav>

<style>
	.cross-links {
		max-width: 72ch;
		margin: var(--space-4) auto 0;
		padding-top: var(--space-3);
		border-top: 1px solid var(--dao-border);
	}

	.cross-links-label {
		font-family: var(--font-sans);
		font-size: var(--type-xs);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		color: var(--dao-muted);
		display: block;
		margin-bottom: var(--space-2);
	}

	.cross-links-list {
		display: flex;
		flex-direction: column;
		gap: var(--space-2);
	}

	.cross-link {
		display: flex;
		align-items: baseline;
		gap: 0.5ch;
		font-family: var(--font-mono);
		font-size: var(--type-base);
		text-decoration: none;
		transition: color var(--duration-fast) var(--easing-linear);
	}

	.link-label {
		font-weight: 600;
		color: var(--dao-text);
	}

	.link-arrow {
		color: var(--dao-muted);
		transition: color var(--duration-fast) var(--easing-linear);
	}

	.link-description {
		color: var(--dao-text-secondary);
	}

	.cross-link-spark:hover .link-label,
	.cross-link-spark:hover .link-arrow {
		color: var(--spark-core);
	}

	.cross-link-emergence:hover .link-label,
	.cross-link-emergence:hover .link-arrow {
		color: var(--emergence-core);
	}

	.cross-link-constraint:hover .link-label,
	.cross-link-constraint:hover .link-arrow {
		color: var(--ci-red);
	}

	@media (prefers-reduced-motion: reduce) {
		.cross-link,
		.link-arrow {
			transition: none;
		}
	}
</style>
