<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<svelte:head>
	<title>{data.metadata?.title || 'Reference'} — cix Library</title>
</svelte:head>

<article class="prose">
	<svelte:component this={data.content} />
</article>

<style>
	.prose {
		max-width: var(--content-width);
	}

	.prose :global(h1) {
		font-size: var(--type-xl);
		margin-bottom: var(--space-3);
	}

	.prose :global(h2) {
		font-size: var(--type-lg);
		margin-top: var(--space-4);
		margin-bottom: var(--space-2);
	}

	.prose :global(h3) {
		font-size: var(--type-base);
		font-weight: 600;
		margin-top: var(--space-3);
		margin-bottom: var(--space-1);
	}

	.prose :global(p) {
		margin-bottom: var(--space-2);
	}

	.prose :global(ul),
	.prose :global(ol) {
		margin-bottom: var(--space-2);
		padding-left: var(--space-3);
	}

	.prose :global(li) {
		margin-bottom: var(--space-1);
	}
</style>
