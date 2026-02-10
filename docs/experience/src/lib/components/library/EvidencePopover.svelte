<script lang="ts">
	import { onMount } from 'svelte';

	type EvidenceLevel = 'strong' | 'moderate' | 'weak' | 'speculative';

	interface Props {
		target: HTMLElement | null;
		level: EvidenceLevel;
		source: string;
		visible: boolean;
		onclose: () => void;
	}

	let { target, level, source, visible, onclose }: Props = $props();

	const LEVEL_LABELS: Record<EvidenceLevel, string> = {
		strong: 'STRONG',
		moderate: 'MODERATE',
		weak: 'WEAK',
		speculative: 'SPECULATIVE'
	};

	const LEVEL_SYMBOLS: Record<EvidenceLevel, string> = {
		strong: '\u25CF',     // ●
		moderate: '\u25D0',   // ◐
		weak: '\u25CB',       // ○
		speculative: '\u25CC' // ◌
	};

	// Position state — computed from target rect
	let x = $state(0);
	let y = $state(0);
	let isMobile = $state(false);
	let popoverEl: HTMLElement | undefined = $state();

	function reposition() {
		if (!target || !popoverEl) return;

		isMobile = window.matchMedia('(max-width: 900px)').matches;
		if (isMobile) return; // Mobile uses fixed bottom sheet, no positioning needed

		const rect = target.getBoundingClientRect();
		const popRect = popoverEl.getBoundingClientRect();

		// Center horizontally on the badge
		let left = rect.left + rect.width / 2 - popRect.width / 2;

		// Clamp to viewport edges with padding
		const pad = 12;
		left = Math.max(pad, Math.min(left, window.innerWidth - popRect.width - pad));

		// Position above the badge
		let top = rect.top - popRect.height - 8;

		// If no room above, flip below
		if (top < pad) {
			top = rect.bottom + 8;
		}

		x = left;
		y = top;
	}

	$effect(() => {
		if (visible && target && popoverEl) {
			// Use rAF to ensure popover is rendered before measuring
			requestAnimationFrame(reposition);
		}
	});

	// Reposition on scroll — dismiss only when badge leaves viewport
	function handleScroll() {
		if (!visible || isMobile || !target) return;
		const rect = target.getBoundingClientRect();
		const inView = rect.top > -rect.height && rect.bottom < window.innerHeight + rect.height;
		if (inView) {
			reposition();
		} else {
			onclose();
		}
	}

	onMount(() => {
		window.addEventListener('scroll', handleScroll, { passive: true });
		return () => window.removeEventListener('scroll', handleScroll);
	});
</script>

{#if visible}
	<!-- svelte-ignore a11y_no_static_element_interactions -->
	<div
		class="ev-popover"
		class:mobile={isMobile}
		data-level={level}
		bind:this={popoverEl}
		style={isMobile ? '' : `left: ${x}px; top: ${y}px;`}
		onkeydown={(e) => { if (e.key === 'Escape') onclose(); }}
	>
		<div class="ev-level">
			<span class="ev-symbol">{LEVEL_SYMBOLS[level]}</span>
			{LEVEL_LABELS[level]}
		</div>
		{#if source}
			<div class="ev-source">{source}</div>
		{/if}
	</div>
{/if}

<style>
	.ev-popover {
		position: fixed;
		z-index: var(--z-popover);

		width: max-content;
		max-width: 320px;

		background: var(--dao-surface-2);
		border: var(--border-width) solid var(--dao-border);
		border-radius: var(--radius-sm);
		padding: var(--space-1) var(--space-1-5);

		font-family: var(--font-mono);
		font-size: var(--type-xs);
		line-height: var(--leading-normal);
		color: var(--dao-text-secondary);
		text-align: left;
		white-space: normal;

		box-shadow: var(--shadow-md);

		animation: ev-fade-in var(--duration-fast) var(--easing-enter);
	}

	/* Caret pointing down (desktop only) */
	.ev-popover:not(.mobile)::after {
		content: '';
		position: absolute;
		top: 100%;
		left: 50%;
		transform: translateX(-50%);
		border: 5px solid transparent;
		border-top-color: var(--dao-border);
	}

	/* Mobile: bottom sheet */
	.ev-popover.mobile {
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		top: auto;
		max-width: 100%;
		border-radius: var(--radius-sm) var(--radius-sm) 0 0;
		padding: var(--space-2) var(--space-3);
	}

	.ev-popover.mobile::after {
		display: none;
	}

	/* --- Content --- */

	.ev-level {
		font-weight: var(--weight-medium);
		text-transform: uppercase;
		letter-spacing: var(--tracking-wider);
		margin-bottom: 2px;
		display: flex;
		align-items: center;
		gap: 0.5ch;
	}

	.ev-source {
		color: var(--dao-muted);
	}

	/* --- Level-specific accent colors --- */

	.ev-popover[data-level='strong'] .ev-level {
		color: var(--ev-strong);
	}

	.ev-popover[data-level='moderate'] .ev-level {
		color: var(--ev-moderate);
	}

	.ev-popover[data-level='weak'] .ev-level {
		color: var(--ev-weak);
	}

	.ev-popover[data-level='speculative'] .ev-level {
		color: var(--ev-speculative);
	}

	/* --- Animation --- */

	@keyframes ev-fade-in {
		from { opacity: 0; }
		to { opacity: 1; }
	}

	@media (prefers-reduced-motion: reduce) {
		.ev-popover {
			animation: none;
		}
	}
</style>
