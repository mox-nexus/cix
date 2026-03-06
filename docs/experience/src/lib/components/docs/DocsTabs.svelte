<script lang="ts">
	interface Props {
		tabs: Array<{ id: string; label: string }>;
		active: string;
		onchange?: (id: string) => void;
	}

	let { tabs, active, onchange }: Props = $props();
</script>

<nav class="tabs" role="tablist">
	{#each tabs as tab}
		<button
			class="tab"
			class:active={active === tab.id}
			role="tab"
			aria-selected={active === tab.id}
			onclick={() => onchange?.(tab.id)}
		>
			{tab.label}
		</button>
	{/each}
</nav>

<style>
	.tabs {
		display: flex;
		gap: 2rem;
		border-bottom: 1px solid var(--dao-border);
		margin-bottom: var(--space-4);
	}

	.tab {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		font-weight: 500;
		letter-spacing: 0.06em;
		text-transform: uppercase;
		color: var(--dao-muted);
		background: none;
		border: none;
		padding: 0 0 0.75rem 0;
		cursor: pointer;
		position: relative;
		transition: color var(--duration-fast) var(--easing-linear);
	}

	.tab:hover {
		color: var(--dao-text);
	}

	.tab.active {
		color: var(--dao-text);
		font-weight: 600;
	}

	.tab.active::after {
		content: '';
		position: absolute;
		bottom: -1px;
		left: 0;
		right: 0;
		height: 2px;
		background: var(--spark-core);
	}

	@media (max-width: 768px) {
		.tabs {
			gap: 1rem;
		}
	}
</style>
