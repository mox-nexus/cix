<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		children?: Snippet;
	}

	let { children }: Props = $props();
</script>

<div class="margin-sw">
	{#if children}
		{@render children()}
	{/if}
</div>

<style>
	.margin-sw {
		/* Southwest margin - manifesto position */
	}
</style>
