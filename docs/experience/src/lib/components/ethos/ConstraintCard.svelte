<script lang="ts">
	interface Props {
		name: string;
		description: string;
		citation: string;
		loopBreaks: string;
		verification: string;
		delay?: number;
	}

	let {
		name,
		description,
		citation,
		loopBreaks,
		verification,
		delay = 0
	}: Props = $props();
</script>

<article class="constraint" style="--stagger-delay: {delay}ms">
	<h3 class="constraint-name">{name}</h3>
	<p class="constraint-description">{description}</p>
	<cite class="constraint-citation">{citation}</cite>
	<p class="constraint-verification">{verification}</p>
	<span class="constraint-loop">{loopBreaks}</span>
</article>

<style>
	.constraint {
		border-left: 3px solid var(--emergence-core);
		padding: var(--space-2) var(--space-3);
		opacity: 0;
		transform: translateY(20px);
		animation: constraint-enter 600ms var(--easing-smooth) forwards;
		animation-delay: var(--stagger-delay, 0ms);
	}

	@keyframes constraint-enter {
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.constraint-name {
		font-family: var(--font-sans);
		font-size: var(--type-lg);
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: var(--tracking-wider);
		color: var(--dao-text);
		margin: 0 0 var(--space-1) 0;
		position: relative;
		display: inline-block;
	}

	.constraint-name::after {
		content: '';
		display: block;
		width: 4ch;
		height: 3px;
		margin-top: var(--space-1);
		background: var(--emergence-core);
		transition: width 300ms var(--easing-smooth);
	}

	.constraint:hover .constraint-name::after {
		width: 100%;
	}

	.constraint-description {
		font-family: var(--font-mono);
		font-size: var(--type-base);
		line-height: var(--leading-relaxed);
		color: var(--dao-text-secondary);
		margin: var(--space-2) 0 0 0;
		max-width: 50ch;
	}

	.constraint-citation {
		display: block;
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		margin-top: var(--space-1);
		font-style: normal;
	}

	.constraint-verification {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: oklch(50% 0.02 240);
		margin: var(--space-1) 0 0 0;
		font-style: italic;
	}

	.constraint-loop {
		display: inline-block;
		font-family: var(--font-sans);
		font-size: var(--type-xs);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		color: var(--emergence-core);
		margin-top: var(--space-1-5);
		padding: var(--space-0-5) var(--space-1);
		border: 1px solid oklch(75% 0.2 145 / 0.2);
		border-radius: var(--radius-sm);
	}

	@media (prefers-reduced-motion: reduce) {
		.constraint {
			opacity: 1;
			transform: none;
			animation: none;
		}

		.constraint-name::after {
			transition: none;
		}
	}
</style>
