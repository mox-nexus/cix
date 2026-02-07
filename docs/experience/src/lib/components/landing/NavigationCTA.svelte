<script lang="ts">
	import { base } from '$app/paths';

	interface Link {
		path: string;
		label: string;
		description: string;
		variant?: 'spark' | 'emergence' | 'constraint';
	}

	interface Props {
		links?: Link[];
	}

	let {
		links = [
			{ path: '/ethos', label: 'ethos', description: 'understand why', variant: 'spark' },
			{ path: '/catalog', label: 'catalog', description: 'explore extensions', variant: 'emergence' },
			{ path: '/library', label: 'library', description: 'deep research', variant: 'constraint' }
		]
	}: Props = $props();
</script>

<nav class="nav-links">
	{#each links as link}
		<a href="{base}{link.path}" class="link link-{link.variant ?? 'spark'}">
			<span class="label">{link.label}</span>
			<span class="arrow">→</span>
			<span class="description">{link.description}</span>
		</a>
	{/each}
</nav>

<style>
	.nav-links {
		display: flex;
		flex-direction: column;
		gap: var(--space-2);
		min-width: 160px;
	}

	.link {
		display: flex;
		align-items: baseline;
		gap: 0.5ch;
		font-family: var(--font-mono);
		font-size: var(--type-base);
		text-decoration: none;
		transition: color var(--duration-fast) var(--easing-linear);
	}

	.label {
		font-weight: 600;
		color: var(--dao-text);
	}

	.arrow {
		color: var(--dao-muted);
		transition: color var(--duration-fast) var(--easing-linear);
	}

	.description {
		color: var(--dao-text-secondary);
	}

	.link-spark:hover .label {
		color: var(--spark-core);
	}

	.link-spark:hover .arrow {
		color: var(--spark-core);
	}

	.link-emergence:hover .label {
		color: var(--emergence-core);
	}

	.link-emergence:hover .arrow {
		color: var(--emergence-core);
	}

	.link-constraint:hover .label {
		color: var(--ci-red);
	}

	.link-constraint:hover .arrow {
		color: var(--ci-red);
	}

	@media (max-width: 768px) {
		.nav-links {
			align-items: center;
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.link {
			transition: none;
		}

		.arrow {
			transition: none;
		}
	}
</style>
