<script lang="ts">
	import '../app.css';

	let { children } = $props();
</script>

<svelte:head>
	<title>cix — Collaborative Intelligence Extensions</title>
	<meta name="description" content="Extensions that enhance human capability, not replace it." />
</svelte:head>

<a href="#main" class="skip-link">Skip to content</a>

<div class="page">
	{@render children()}
</div>
