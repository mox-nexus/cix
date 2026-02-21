<script lang="ts">
	import { base } from '$app/paths';

	interface Link {
		path: string;
		label: string;
		variant?: 'spark' | 'emergence' | 'reference';
	}

	interface Props {
		links?: Link[];
	}

	let {
		links = [
			{ path: '/catalog', label: 'catalog', variant: 'spark' },
			{ path: '/library', label: 'docs', variant: 'reference' }
		]
	}: Props = $props();
</script>

<nav class="nav-links">
	{#each links as link}
		<a href="{base}{link.path}" class="link link-{link.variant ?? 'spark'}">
			<span class="label">{link.label}</span>
			<span class="arrow">→</span>
		</a>
	{/each}
</nav>

<style>
	.nav-links {
		display: flex;
		flex-direction: column;
		align-items: flex-end;
		gap: var(--space-2);
	}

	.link {
		display: flex;
		align-items: baseline;
		gap: 0.5ch;
		font-family: var(--font-mono);
		font-size: var(--type-lg);
		text-decoration: none;
		transition: color var(--duration-fast) var(--easing-linear);
	}

	.label {
		font-weight: 400;
	}

	.arrow {
		transition: transform var(--duration-fast) var(--easing-linear),
		            color var(--duration-fast) var(--easing-linear);
		display: inline-block;
	}

	/* Spark (catalog) — blue */
	.link-spark .label  { color: var(--spark-core); }
	.link-spark .arrow  { color: oklch(75% 0.18 240 / 0.45); }
	.link-spark:hover .label,
	.link-spark:hover .arrow { color: var(--spark-core); }

	/* Emergence (ethos) — green */
	.link-emergence .label  { color: var(--emergence-core); }
	.link-emergence .arrow  { color: oklch(75% 0.2 145 / 0.45); }
	.link-emergence:hover .label,
	.link-emergence:hover .arrow { color: var(--emergence-core); }

	/* Reference (docs) — indigo */
	.link-reference .label  { color: var(--quadrant-reference); }
	.link-reference .arrow  { color: oklch(68% 0.10 290 / 0.45); }
	.link-reference:hover .label,
	.link-reference:hover .arrow { color: var(--quadrant-reference); }

	/* Hover: arrow nudges right */
	.link:hover .arrow {
		transform: translateX(0.3ch);
	}

	.link:focus-visible {
		outline: 1px solid currentColor;
		outline-offset: 4px;
		border-radius: var(--radius-sm);
	}

	@media (max-width: 768px) {
		.nav-links {
			align-items: center;
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.link, .arrow {
			transition: none;
		}
	}
</style>
