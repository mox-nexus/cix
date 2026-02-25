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
		<p>
			How you use AI determines whether
			it compounds your craft or erodes it.
		</p>
		<p class="hook">
			<span class="extend">Extend your mind,</span>
			<span class="replace">don't replace it.</span>
		</p>
	{/if}
</aside>

<style>
	.philosophy {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		justify-content: center;
		gap: var(--space-3);
		height: 100%;
		text-align: left;
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
		font-size: var(--type-lg);
		margin: var(--space-3) 0 0;
		line-height: var(--leading-snug);
	}

	.extend {
		color: var(--spark-core);
		font-weight: 600;
	}

	.replace {
		color: var(--ci-red);
		font-weight: 600;
	}

	.philosophy :global(p) {
		font-family: var(--font-mono);
		font-size: var(--type-base);
		color: var(--dao-text-secondary);
		line-height: var(--leading-relaxed);
		margin: 0;
	}
</style>
