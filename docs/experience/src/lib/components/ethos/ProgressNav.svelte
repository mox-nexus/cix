<script lang="ts">
	import { scrollTo } from '$lib/stores/scroll';

	let {
		sections,
		currentSection
	}: {
		sections: { id: string; title: string }[];
		currentSection: string | null;
	} = $props();
</script>

<nav class="progress-nav" aria-label="Section navigation">
	<ol class="progress-list">
		{#each sections as section}
			<li class="progress-item">
				<button
					class="progress-button"
					class:active={currentSection === section.id}
					onclick={() => scrollTo(`#${section.id}`)}
					aria-current={currentSection === section.id ? 'step' : undefined}
				>
					<span class="progress-dot"></span>
					<span class="progress-label">{section.title}</span>
				</button>
			</li>
		{/each}
	</ol>
</nav>

<style>
	.progress-nav {
		position: fixed;
		right: var(--space-3);
		top: 50%;
		transform: translateY(-50%);
		z-index: 100;
	}

	.progress-list {
		list-style: none;
		padding: 0;
		margin: 0;
		display: flex;
		flex-direction: column;
		gap: var(--space-2);
	}

	.progress-item {
		display: flex;
		align-items: center;
	}

	.progress-button {
		display: flex;
		align-items: center;
		gap: var(--space-1);
		background: none;
		border: none;
		cursor: pointer;
		padding: var(--space-1);
		color: var(--dao-muted);
		transition: color var(--duration-fast) var(--easing-linear);
	}

	.progress-button:hover,
	.progress-button.active {
		color: var(--dao-text);
	}

	.progress-dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		background: var(--dao-border);
		transition: background var(--duration-fast) var(--easing-linear),
		            transform var(--duration-fast) var(--easing-out);
	}

	.progress-button:hover .progress-dot {
		background: var(--dao-muted);
	}

	.progress-button.active .progress-dot {
		background: var(--emergence-core);
		transform: scale(1.25);
	}

	.progress-label {
		font-size: var(--type-xs);
		white-space: nowrap;
		opacity: 0;
		transform: translateX(-4px);
		transition: opacity var(--duration-fast) var(--easing-linear),
		            transform var(--duration-fast) var(--easing-out);
	}

	.progress-button:hover .progress-label,
	.progress-button.active .progress-label {
		opacity: 1;
		transform: translateX(0);
	}

	/* Hide on mobile */
	@media (max-width: 768px) {
		.progress-nav {
			display: none;
		}
	}

	/* Reduced motion */
	@media (prefers-reduced-motion: reduce) {
		.progress-dot,
		.progress-label {
			transition: none;
		}
	}
</style>
