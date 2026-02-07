import { writable, derived } from 'svelte/store';
import { browser } from '$app/environment';

// Scroll progress (0-1)
export const scrollProgress = writable(0);

// Current active section
export const currentSection = writable<string | null>(null);

// Reduced motion preference
export const prefersReducedMotion = writable(false);

// Initialize reduced motion detection
if (browser) {
	const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
	prefersReducedMotion.set(mediaQuery.matches);

	mediaQuery.addEventListener('change', (e) => {
		prefersReducedMotion.set(e.matches);
	});
}

// Lenis instance holder (set by ethos page)
export let lenisInstance: any = null;

export function setLenisInstance(lenis: any) {
	lenisInstance = lenis;
}

export function scrollTo(target: string | number) {
	if (lenisInstance) {
		lenisInstance.scrollTo(target, { duration: 1.2 });
	} else if (browser) {
		// Fallback for non-Lenis pages
		if (typeof target === 'string') {
			document.querySelector(target)?.scrollIntoView({ behavior: 'smooth' });
		} else {
			window.scrollTo({ top: target, behavior: 'smooth' });
		}
	}
}
