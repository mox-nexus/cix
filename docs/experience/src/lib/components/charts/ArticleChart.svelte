<script lang="ts">
	import NamingConvergence from './NamingConvergence.svelte';

	const charts: Record<string, typeof NamingConvergence> = {
		'naming-convergence': NamingConvergence
	};

	let { id = '', ...rest }: { id?: string } = $props();

	const Chart = $derived(id ? charts[id] : undefined);
</script>

{#if Chart}
	<Chart {...rest} />
{:else}
	<p style="color: #f44; font-style: italic;">Unknown chart: {id}</p>
{/if}
