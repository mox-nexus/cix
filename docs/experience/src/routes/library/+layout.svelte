<script lang="ts">
	import Sidebar from '$lib/components/library/Sidebar.svelte';

	let { children } = $props();
</script>

<div class="library-layout">
	<aside class="sidebar-container">
		<Sidebar />
	</aside>

	<main id="main" class="main-content">
		{@render children()}
	</main>
</div>

<style>
	.library-layout {
		display: grid;
		grid-template-columns: var(--sidebar-width) 1fr;
		min-height: 100vh;
		min-height: 100dvh;
	}

	.sidebar-container {
		background: var(--dao-surface);
		border-right: var(--border-width) solid var(--dao-border);
	}

	.main-content {
		padding: var(--space-4);
		max-width: var(--content-width);
	}

	/* Mobile: collapse sidebar */
	@media (max-width: 768px) {
		.library-layout {
			grid-template-columns: 1fr;
		}

		.sidebar-container {
			display: none;
		}
	}
</style>
