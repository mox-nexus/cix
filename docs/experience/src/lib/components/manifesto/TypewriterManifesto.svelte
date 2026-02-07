<script lang="ts">
	import { onMount } from 'svelte';

	// Configurable props with defaults
	interface Props {
		words?: string[];
		staticLines?: { text: string; color: 'red' | 'blue' | 'green' }[];
		typingSpeed?: number;
		holdDuration?: number;
	}

	let {
		words = ['nonconformity', 'ideas', 'effort'],
		staticLines = [
			{ text: 'AMPLIFY', color: 'red' },
			{ text: 'RADICAL', color: 'blue' }
		],
		typingSpeed = 80,
		holdDuration = 1500
	}: Props = $props();

	// Typewriter state
	let currentWordIndex = $state(0);
	let displayedChars = $state(0);
	let isTyping = $state(true);
	let prefersReducedMotion = $state(false);

	let currentWord = $derived(words[currentWordIndex]);
	// If reduced motion, show full word immediately
	let displayedText = $derived(
		prefersReducedMotion ? currentWord : currentWord.slice(0, displayedChars)
	);

	onMount(() => {
		// Check motion preference (accessibility)
		const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
		prefersReducedMotion = motionQuery.matches;

		// Listen for preference changes
		const handleMotionChange = (e: MediaQueryListEvent) => {
			prefersReducedMotion = e.matches;
			if (e.matches) {
				// Show full word immediately when reduced motion enabled
				displayedChars = words[currentWordIndex].length;
			}
		};
		motionQuery.addEventListener('change', handleMotionChange);

		// If reduced motion, still cycle words but without typing animation
		const typeInterval = setInterval(() => {
			if (prefersReducedMotion) {
				// Just cycle words without typing effect
				if (!isTyping) return;
				isTyping = false;
				setTimeout(() => {
					currentWordIndex = (currentWordIndex + 1) % words.length;
					isTyping = true;
				}, holdDuration);
				return;
			}

			// Normal typewriter effect
			const word = words[currentWordIndex];
			if (isTyping) {
				if (displayedChars < word.length) {
					displayedChars++;
				} else {
					isTyping = false;
					setTimeout(() => {
						currentWordIndex = (currentWordIndex + 1) % words.length;
						displayedChars = 0;
						isTyping = true;
					}, holdDuration);
				}
			}
		}, typingSpeed);

		return () => {
			clearInterval(typeInterval);
			motionQuery.removeEventListener('change', handleMotionChange);
		};
	});
</script>

<div class="manifesto">
	{#each staticLines as line}
		<div class="word word-{line.color}">{line.text}</div>
	{/each}
	<div class="word word-emergence">
		<span class="typed-text">{displayedText}</span>{#if !prefersReducedMotion}<span class="caret" class:typing={isTyping}>|</span>{/if}
	</div>
</div>

<style>
	/*
	 * TYPEWRITER MANIFESTO
	 *
	 * Stacked dialectical statement with animated emergence.
	 * Red (constraint/machine) → Blue (spark/human) → Green (emergence/synthesis)
	 */

	.manifesto {
		display: flex;
		flex-direction: column;
		gap: 0;
		font-family: var(--font-sans);
		font-size: var(--type-lg);
		font-weight: 700;
		letter-spacing: var(--tracking-wide);
		line-height: 1.2;
	}

	/* RED - constraint, the machine that amplifies */
	.word-red {
		color: var(--ci-red);
		text-shadow:
			0 0 4px oklch(58% 0.18 25 / 0.6),
			0 0 12px oklch(50% 0.15 25 / 0.3);
	}

	/* BLUE - spark, human agency */
	.word-blue {
		color: var(--spark-core);
		text-shadow:
			0 0 4px oklch(62% 0.15 240 / 0.6),
			0 0 12px oklch(55% 0.12 240 / 0.3),
			0 0 24px oklch(50% 0.08 240 / 0.15);
	}

	/* GREEN - emergence/synthesis */
	.word-green,
	.word-emergence {
		color: var(--emergence-core);
		text-shadow:
			0 0 4px oklch(70% 0.18 145 / 0.5),
			0 0 12px oklch(65% 0.12 145 / 0.2);
		min-height: 1.2em;
	}

	.caret {
		color: var(--emergence-core);
		animation: blink 0.6s step-end infinite;
	}

	.caret:not(.typing) {
		animation: none;
		opacity: 0;
	}

	@keyframes blink {
		50% { opacity: 0; }
	}

	/* -----------------------------------------
	   REDUCED MOTION
	   ----------------------------------------- */

	@media (prefers-reduced-motion: reduce) {
		.word-red,
		.word-blue,
		.word-green,
		.word-emergence {
			text-shadow: none;
		}

		.caret {
			animation: none;
		}
	}
</style>
