<script lang="ts">
	let { children } = $props();
</script>

<main id="main" class="library-layout">
	{@render children()}
</main>

<style>
	.library-layout {
		min-height: 100vh;
		min-height: 100dvh;
		background: var(--dao-bg);
		padding: var(--space-4) var(--space-3);
	}
</style>
