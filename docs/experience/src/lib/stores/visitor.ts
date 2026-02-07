import { writable, derived } from 'svelte/store';
import { browser } from '$app/environment';

const VISITOR_KEY = 'cix-visitor-state';
const VISIT_THRESHOLD = 3;

interface VisitorState {
	firstVisit: string | null;
	lastVisit: string | null;
	visitCount: number;
	expressMode: boolean;
}

const defaultState: VisitorState = {
	firstVisit: null,
	lastVisit: null,
	visitCount: 0,
	expressMode: false
};

function loadState(): VisitorState {
	if (!browser) return defaultState;
	try {
		const stored = localStorage.getItem(VISITOR_KEY);
		if (stored) {
			return { ...defaultState, ...JSON.parse(stored) };
		}
	} catch {
		// Invalid storage
	}
	return defaultState;
}

function saveState(state: VisitorState): void {
	if (!browser) return;
	try {
		localStorage.setItem(VISITOR_KEY, JSON.stringify(state));
	} catch {
		// Storage full or blocked
	}
}

function createVisitorStore() {
	const initial = loadState();

	// Record this visit
	const now = new Date().toISOString();
	const updated: VisitorState = {
		...initial,
		firstVisit: initial.firstVisit || now,
		lastVisit: now,
		visitCount: initial.visitCount + 1
	};

	const { subscribe, set, update } = writable(updated);

	// Persist on changes
	subscribe(saveState);

	return {
		subscribe,

		setExpressMode: (enabled: boolean) => {
			update(s => ({ ...s, expressMode: enabled }));
		},

		reset: () => {
			set({ ...defaultState, firstVisit: new Date().toISOString(), visitCount: 1 });
		}
	};
}

export const visitor = createVisitorStore();

// Derived stores
export const isReturningVisitor = derived(
	visitor,
	$v => $v.visitCount >= VISIT_THRESHOLD
);

export const isExpressMode = derived(
	visitor,
	$v => $v.expressMode || $v.visitCount >= VISIT_THRESHOLD
);

export const visitCount = derived(
	visitor,
	$v => $v.visitCount
);
