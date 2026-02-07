<script lang="ts">
	import type { Snippet } from 'svelte';

	let {
		title = 'Constraint',
		children
	}: {
		title?: string;
		children: Snippet;
	} = $props();
</script>

<aside class="constraint-block" role="note" aria-label={title}>
	<header class="constraint-header">
		<span class="constraint-marker" aria-hidden="true"></span>
		<strong class="constraint-title">{title}</strong>
	</header>
	<div class="constraint-content">
		{@render children()}
	</div>
</aside>

<style>
	.constraint-block {
		position: relative;
		margin-block: var(--space-4);
		padding: var(--space-3);
		padding-left: var(--space-4);
		background: linear-gradient(
			90deg,
			oklch(58% 0.18 25 / 0.04) 0%,
			transparent 50%
		);
		border-left: 3px solid var(--dao-red);
		border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
	}

	.constraint-header {
		display: flex;
		align-items: center;
		gap: var(--space-1);
		margin-bottom: var(--space-2);
	}

	/* Square marker for constraint (vs circle for emergence) */
	.constraint-marker {
		width: 6px;
		height: 6px;
		background: var(--dao-red);
	}

	.constraint-title {
		font-family: var(--font-sans);
		font-size: var(--type-sm);
		color: var(--dao-red);
		text-transform: uppercase;
		letter-spacing: var(--tracking-wide);
	}

	.constraint-content {
		color: var(--dao-muted);
		font-size: var(--type-sm);
	}

	.constraint-content :global(p:first-child) {
		margin-top: 0;
	}

	.constraint-content :global(p:last-child) {
		margin-bottom: 0;
	}
</style>
