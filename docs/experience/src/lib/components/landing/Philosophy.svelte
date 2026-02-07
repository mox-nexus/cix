<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		children?: Snippet;
	}

	let { children }: Props = $props();
</script>

<aside class="philosophy">
	{#if children}
		{@render children()}
	{:else}
		<blockquote class="quote">
			"A competent programmer is fully aware of the strictly limited size of his own skull."
			<cite>Dijkstra</cite>
		</blockquote>
		<p class="hook"><em>Extend it.</em></p>
		<p>
			Agency + intelligence =
			capability that compounds.
			Extensions that sharpen, not substitute.
		</p>
	{/if}
</aside>

<style>
	.philosophy {
		display: flex;
		flex-direction: column;
		align-items: flex-end;
		justify-content: center;
		gap: var(--space-2);
		height: 100%;
		text-align: right;
		min-width: 200px;
	}

	.quote {
		font-family: var(--font-mono);
		font-size: var(--type-base);
		color: var(--dao-text-secondary);
		line-height: var(--leading-relaxed);
		margin: 0;
		font-style: italic;
	}

	.philosophy :global(cite) {
		display: block;
		font-size: var(--type-sm);
		color: var(--spark-core);
		font-style: normal;
		margin-top: var(--space-0-5);
	}

	.hook {
		font-family: var(--font-mono);
		font-size: var(--type-xl);
		margin: 0;
	}

	.philosophy :global(p) {
		font-family: var(--font-mono);
		font-size: var(--type-base);
		color: var(--dao-text-secondary);
		line-height: var(--leading-relaxed);
		margin: 0;
	}

	.philosophy :global(em) {
		color: var(--emergence-core);
		font-style: normal;
		font-weight: 600;
	}
</style>
