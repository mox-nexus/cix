<script lang="ts">
	import type { Snippet } from 'svelte';

	let {
		title,
		children
	}: {
		title?: string;
		children: Snippet;
	} = $props();
</script>

<aside class="emergence-block" aria-label={title || 'Emergent synthesis'}>
	{#if title}
		<header class="emergence-header">
			<span class="emergence-marker" aria-hidden="true"></span>
			<strong class="emergence-title">{title}</strong>
		</header>
	{/if}
	<div class="emergence-content">
		{@render children()}
	</div>
</aside>

<style>
	.emergence-block {
		position: relative;
		margin-block: var(--pause-dramatic);
		padding: var(--space-3);
		padding-left: var(--space-4);
		background: linear-gradient(
			90deg,
			oklch(70% 0.18 145 / 0.04) 0%,
			transparent 60%
		);
		border-left: 3px solid var(--emergence-core);
		border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
	}

	.emergence-header {
		display: flex;
		align-items: center;
		gap: var(--space-1);
		margin-bottom: var(--space-2);
	}

	.emergence-marker {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		background: var(--emergence-core);
		box-shadow:
			0 0 4px var(--emergence-glow),
			0 0 12px var(--emergence-glow);
	}

	.emergence-title {
		font-family: var(--font-sans);
		font-size: var(--type-sm);
		color: var(--emergence-core);
		text-transform: uppercase;
		letter-spacing: var(--tracking-wide);
	}

	.emergence-content {
		color: var(--dao-text);
	}

	.emergence-content :global(p:first-child) {
		margin-top: 0;
	}

	.emergence-content :global(p:last-child) {
		margin-bottom: 0;
	}

	/* Reduced motion: remove glow from marker */
	@media (prefers-reduced-motion: reduce) {
		.emergence-marker {
			box-shadow: none;
		}
	}
</style>
