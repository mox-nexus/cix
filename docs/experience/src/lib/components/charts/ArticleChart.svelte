<script lang="ts">
	import NamingConvergence from './NamingConvergence.svelte';
	import BastaniSplit from './BastaniSplit.svelte';
	import DesignLeverHierarchy from './DesignLeverHierarchy.svelte';
	import DiversityParadox from './DiversityParadox.svelte';

	const charts: Record<string, typeof NamingConvergence> = {
		'naming-convergence': NamingConvergence,
		'bastani-split': BastaniSplit,
		'design-lever-hierarchy': DesignLeverHierarchy,
		'diversity-paradox': DiversityParadox
	};

	let { id = '', ...rest }: { id?: string } = $props();

	const Chart = $derived(id ? charts[id] : undefined);
</script>

{#if Chart}
	<Chart {...rest} />
{:else}
	<p style="color: #f44; font-style: italic;">Unknown chart: {id}</p>
{/if}
