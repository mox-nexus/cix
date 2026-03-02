/**
 * Scroll-to-beat mapping for the ethos experience.
 * 5 beats across 590vh of scroll distance.
 *
 * Pacing: Foundations breathes, Shift hits fast, Compounding has
 * the most room (three ideas need air), Duty holds weight, Invitation settles.
 */

export interface BeatState {
	beat: number; // 1-5
	t: number; // 0-1 normalized progress within beat
}

// Beat section heights in viewport multiples
// 1.2 + 0.8 + 1.4 + 1.3 + 1.2 = 5.9
const BEATS = [
	{ start: 0, end: 1.2 }, // Beat 1: 120vh — Foundations (breathing room)
	{ start: 1.2, end: 2.0 }, // Beat 2:  80vh — The Shift (short, punchy)
	{ start: 2.0, end: 3.4 }, // Beat 3: 140vh — The Compounding (longest)
	{ start: 3.4, end: 4.7 }, // Beat 4: 130vh — The Duty (weight)
	{ start: 4.7, end: 5.9 } // Beat 5: 120vh — The Invitation (settle)
] as const;

export const TOTAL_SCROLL_VH = 590;

export function smoothstep(t: number): number {
	const c = Math.max(0, Math.min(1, t));
	return c * c * (3 - 2 * c);
}

export function lerp(a: number, b: number, t: number): number {
	return a + (b - a) * Math.max(0, Math.min(1, t));
}

export function scrollToBeat(scrollY: number, vh: number): BeatState {
	const scrollViewports = scrollY / vh;

	for (let i = 0; i < BEATS.length; i++) {
		const { start, end } = BEATS[i];
		if (scrollViewports < end) {
			const t = Math.max(0, Math.min(1, (scrollViewports - start) / (end - start)));
			return { beat: i + 1, t };
		}
	}

	return { beat: 5, t: 1 };
}
