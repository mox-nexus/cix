<script lang="ts">
	import { setContext } from 'svelte';
	import type { Snippet } from 'svelte';

	let {
		id,
		children,
		visual
	}: {
		id: string;
		children: Snippet;
		visual?: Snippet;
	} = $props();

	let progress = $state(0);
	let isActive = $state(false);

	// Expose context to child components
	setContext('scene', {
		get progress() { return progress; },
		get isActive() { return isActive; },
		id
	});

	// Allow external progress updates
	export function setProgress(p: number) {
		progress = p;
		isActive = p > 0 && p < 1;
	}
</script>

<section class="scrolly-section" data-scene={id} {id}>
	{#if visual}
		<div class="sticky-visual">
			<figure class="visual-content">
				{@render visual()}
			</figure>
		</div>
	{/if}

	<div class="scroll-content">
		{@render children()}
	</div>
</section>

<style>
	.scrolly-section {
		position: relative;
		display: flex;
		min-height: 150vh;
		gap: var(--space-4);
	}

	.sticky-visual {
		position: sticky;
		top: 0;
		height: 100vh;
		height: 100dvh;
		flex: 1;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: var(--space-4);
	}

	.visual-content {
		width: 100%;
		max-width: 600px;
		margin: 0;
	}

	.scroll-content {
		flex: 1;
		max-width: var(--content-width);
		padding: var(--space-6) var(--space-3);
		display: flex;
		flex-direction: column;
		justify-content: center;
	}

	/* Mobile: stack vertically */
	@media (max-width: 768px) {
		.scrolly-section {
			flex-direction: column;
			min-height: auto;
		}

		.sticky-visual {
			position: relative;
			height: auto;
			min-height: 50vh;
		}

		.scroll-content {
			padding: var(--space-4) var(--space-2);
		}
	}
</style>
