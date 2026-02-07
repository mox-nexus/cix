<script lang="ts">
	import type { Snippet } from 'svelte';

	let {
		children
	}: {
		children: Snippet;
	} = $props();
</script>

<div class="research-table">
	{@render children()}
</div>

<style>
	.research-table {
		margin: var(--space-2) 0;
	}

	.research-table :global(table) {
		width: 100%;
		border-collapse: collapse;
	}

	.research-table :global(td.positive),
	.research-table :global(.positive) {
		color: var(--emergence-core);
	}

	.research-table :global(td.negative),
	.research-table :global(.negative) {
		color: var(--ci-red);
	}

	.research-table :global(td.citation),
	.research-table :global(.citation) {
		font-size: var(--type-sm);
		color: var(--dao-muted);
		font-style: normal;
	}
</style>
