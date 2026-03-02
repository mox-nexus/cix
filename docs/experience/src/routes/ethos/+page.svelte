<svelte:head>
	<title>ethos — cix</title>
</svelte:head>

<main class="under-construction">
	<p class="label">ethos</p>
	<p class="status">under construction</p>
</main>

<style>
	.under-construction {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		min-height: 60vh;
		gap: var(--space-2);
	}

	.label {
		font-family: var(--font-sans);
		font-size: var(--type-2xl);
		font-weight: 700;
		color: var(--dao-text);
	}

	.status {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
	}
</style>
