<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		children?: Snippet;
	}

	let { children }: Props = $props();
</script>

<div class="margin-se">
	{#if children}
		{@render children()}
	{/if}
</div>

<style>
	.margin-se {
		/* Southeast margin - reserved */
	}
</style>
