<script lang="ts">
	import { onMount } from 'svelte';

	let {
		headings = []
	}: {
		headings: { id: string; text: string; level: number }[];
	} = $props();

	let activeId = $state('');

	onMount(() => {
		if (headings.length === 0) return;

		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						activeId = entry.target.id;
					}
				});
			},
			{ rootMargin: '-20% 0% -70% 0%' }
		);

		headings.forEach(({ id }) => {
			const el = document.getElementById(id);
			if (el) observer.observe(el);
		});

		return () => observer.disconnect();
	});
</script>

{#if headings.length > 0}
	<nav class="toc" aria-label="Table of contents">
		<h4 class="toc-title">On this page</h4>
		<ul class="toc-list">
			{#each headings as { id, text, level }}
				<li>
					<a
						href="#{id}"
						class="toc-link"
						class:active={activeId === id}
						style="padding-left: {(level - 2) * 12}px"
					>
						{text}
					</a>
				</li>
			{/each}
		</ul>
	</nav>
{/if}

<style>
	.toc {
		padding: var(--space-3);
		position: sticky;
		top: var(--space-4);
	}

	.toc-title {
		font-size: var(--type-sm);
		color: var(--dao-muted);
		text-transform: uppercase;
		letter-spacing: var(--tracking-wide);
		margin: 0 0 var(--space-2);
	}

	.toc-list {
		list-style: none;
		padding: 0;
		margin: 0;
	}

	.toc-link {
		display: block;
		padding: 4px 0;
		font-size: var(--type-xs);
		color: var(--dao-muted);
		border-bottom: none;
		transition: color var(--duration-fast) var(--easing-linear);
	}

	.toc-link:hover {
		color: var(--dao-text);
	}

	.toc-link.active {
		color: var(--spark-core);
	}
</style>
