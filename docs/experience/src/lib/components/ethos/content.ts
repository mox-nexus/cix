/**
 * Beat content for the ethos experience.
 * Conviction content — not research, not evidence. Belief.
 *
 * Three Doors weave through:
 *   Door 3 (ground) → Door 1 (principle) → Door 2 (constituency) → Door 3 (circle closes)
 *
 * Beat 5 register: matter-of-fact. Almost shrugging. The conviction is so deep
 * it doesn't perform itself. "What else you gonna do?" — plain. Obvious. Done.
 */

export interface BeatContent {
	id: number;
	lines: ContentLine[];
}

export interface ContentLine {
	text: string;
	font: 'sans' | 'mono';
	size: 'display' | 'hero' | 'heading' | 'body' | 'small';
	accent?: 'spark' | 'constraint' | 'emergence' | 'muted';
	weight?: number;
	spacing?: string; // margin-top
}

export const BEATS: BeatContent[] = [
	{
		id: 1,
		// FOUNDATIONS — Door 3 entry. The specific, undeniable thing.
		// First line lands alone: you are already in the mechanism.
		// Second line names the mechanism — not personal legacy, structural compounding.
		lines: [
			{
				text: 'Every line of code you wrote today ran on someone else\u2019s decade.',
				font: 'sans',
				size: 'hero',
				weight: 600
			},
			{
				text: 'That\u2019s not gratitude. That\u2019s how it compounds.',
				font: 'mono',
				size: 'body',
				accent: 'muted',
				spacing: 'var(--space-3)'
			}
		]
	},
	{
		id: 2,
		// THE CROSSING — Door 3 → Door 1.
		// Specific inheritance flips to universal structural truth.
		// Hold it alone. Let it complete.
		lines: [
			{
				text: 'Now we\u2019re all giants.',
				font: 'sans',
				size: 'display',
				weight: 700
			}
		]
	},
	{
		id: 3,
		// THE WEIGHT ARRIVES — Door 1 → Door 3.
		// Being a giant means you're someone else's foundation.
		// Lines stagger in — the landing IS the acceleration.
		// Bastani fact: the crossing from principle to embodied recognition.
		lines: [
			{
				text: 'Giants standing on the shoulders of giants.',
				font: 'sans',
				size: 'hero',
				weight: 600
			},
			{
				text: 'Being a giant means you\u2019re someone else\u2019s foundation.',
				font: 'mono',
				size: 'body',
				accent: 'spark',
				spacing: 'var(--space-3)'
			},
			{
				text: 'Developers who offloaded thinking to AI scored two letter grades lower afterward.',
				font: 'mono',
				size: 'body',
				accent: 'constraint',
				spacing: 'var(--space-2)'
			},
			{
				text: 'They didn\u2019t know.',
				font: 'mono',
				size: 'body',
				accent: 'constraint',
				spacing: 'var(--space-1)'
			}
		]
	},
	{
		id: 4,
		// THE DESIGN QUESTION — Door 2. Every builder is making this choice right now.
		// Not a clean binary — the difference is directional and it accumulates.
		// "Forecloses / amplifies" are conditional: patterns THAT do X compound.
		// Not claiming every pattern is one or the other.
		lines: [
			{
				text: 'Same tool.',
				font: 'sans',
				size: 'heading',
				weight: 700
			},
			{
				text: 'Different design.',
				font: 'sans',
				size: 'heading',
				weight: 700,
				spacing: 'var(--space-1)'
			},
			{
				text: 'The difference compounds.',
				font: 'sans',
				size: 'heading',
				accent: 'emergence',
				weight: 700,
				spacing: 'var(--space-1)'
			},
			{
				text: 'Every pattern that forecloses capability compounds.',
				font: 'mono',
				size: 'body',
				accent: 'constraint',
				spacing: 'var(--space-4)'
			},
			{
				text: 'Every pattern that amplifies it compounds.',
				font: 'mono',
				size: 'body',
				accent: 'emergence',
				spacing: 'var(--space-1)'
			}
		]
	},
	{
		id: 5,
		// THE CLOSE — Door 2 → Door 3. Matter-of-fact. Almost shrugging.
		// Principles named as imperatives — what building right means.
		// Not a call to action. A position stated. The reader is already in it.
		// cix → link follows naturally. Not a pitch. An answer.
		lines: [
			{
				text: 'You don\u2019t leave things worse than you found them.',
				font: 'sans',
				size: 'heading',
				weight: 600
			},
			{
				text: 'Not as preference. As consequence.',
				font: 'mono',
				size: 'body',
				accent: 'muted',
				spacing: 'var(--space-3)'
			},
			{
				text: 'Amplify, don\u2019t replace.',
				font: 'mono',
				size: 'body',
				accent: 'spark',
				spacing: 'var(--space-2)'
			},
			{
				text: 'Show the reasoning. Compound the value.',
				font: 'mono',
				size: 'body',
				accent: 'spark',
				spacing: 'var(--space-1)'
			},
			{
				text: 'Build the ecosystem.',
				font: 'sans',
				size: 'hero',
				accent: 'emergence',
				weight: 700,
				spacing: 'var(--space-4)'
			},
			{
				text: 'What else you gonna do?',
				font: 'mono',
				size: 'body',
				accent: 'muted',
				spacing: 'var(--space-3)'
			}
		]
	}
];
