import { writable, derived } from 'svelte/store';
import { browser } from '$app/environment';

const STORAGE_KEY = 'cix-reading-progress';

export type ReadingState = 'unvisited' | 'visited' | 'completed';

interface ReadingProgress {
	/** slug → state */
	entries: Record<string, ReadingState>;
}

const defaultProgress: ReadingProgress = {
	entries: {}
};

function loadProgress(): ReadingProgress {
	if (!browser) return defaultProgress;
	try {
		const stored = localStorage.getItem(STORAGE_KEY);
		if (stored) {
			return { ...defaultProgress, ...JSON.parse(stored) };
		}
	} catch {
		// Invalid storage
	}
	return defaultProgress;
}

function saveProgress(progress: ReadingProgress): void {
	if (!browser) return;
	try {
		localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
	} catch {
		// Storage full or blocked
	}
}

function createReadingProgressStore() {
	const { subscribe, update } = writable(loadProgress());

	// Persist on changes
	subscribe(saveProgress);

	return {
		subscribe,

		/** Auto-called when article page loads */
		markVisited(slug: string) {
			update((p) => {
				const current = p.entries[slug];
				// Don't downgrade completed → visited
				if (current === 'completed') return p;
				return {
					...p,
					entries: { ...p.entries, [slug]: 'visited' }
				};
			});
		},

		/** Explicit user action — "I've read this" */
		markCompleted(slug: string) {
			update((p) => ({
				...p,
				entries: { ...p.entries, [slug]: 'completed' }
			}));
		},

		/** Toggle completed ↔ visited */
		toggleCompleted(slug: string) {
			update((p) => {
				const current = p.entries[slug] || 'unvisited';
				const next = current === 'completed' ? 'visited' : 'completed';
				return {
					...p,
					entries: { ...p.entries, [slug]: next }
				};
			});
		},

		/** Reset all progress */
		reset() {
			update(() => defaultProgress);
		}
	};
}

export const readingProgress = createReadingProgressStore();

// --- Derived stores ---

/** Get reading state for a specific article */
export function getReadingState(slug: string) {
	return derived(readingProgress, ($p) => $p.entries[slug] || 'unvisited');
}

/** Overview stats */
export const readingOverview = derived(readingProgress, ($p) => {
	const states = Object.values($p.entries);
	return {
		visited: states.filter((s) => s === 'visited').length,
		completed: states.filter((s) => s === 'completed').length,
		total: states.length
	};
});
