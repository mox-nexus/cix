<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { base } from '$app/paths';
	import ScrollySection from '$lib/components/ethos/ScrollySection.svelte';
	import Step from '$lib/components/ethos/Step.svelte';
	import ProgressNav from '$lib/components/ethos/ProgressNav.svelte';
	import DuelingStat from '$lib/components/ethos/DuelingStat.svelte';
	import ExtendedMindDiagram from '$lib/components/ethos/ExtendedMindDiagram.svelte';
	import ConstraintCard from '$lib/components/ethos/ConstraintCard.svelte';
	import ResearchTable from '$lib/components/ethos/ResearchTable.svelte';
	import { setLenisInstance, prefersReducedMotion, currentSection } from '$lib/stores/scroll';

	// Section definitions
	const sections = [
		{ id: 'illusion', title: 'The Productivity Illusion' },
		{ id: 'hollowing', title: 'The Hollowing Problem' },
		{ id: 'homogenization', title: 'Homogenization' },
		{ id: 'collaboration', title: 'What Makes Collaboration Work' },
		{ id: 'trust', title: 'The Trust Paradox' },
		{ id: 'complementary', title: 'Complementary vs Substitutive' },
		{ id: 'cognition', title: 'Cognitive Extensions' },
		{ id: 'constraints', title: 'Design Constraints' },
		{ id: 'goal', title: 'The Goal' }
	];

	let activeSection = $state<string | null>('illusion');
	let reducedMotion = $state(false);

	// Subscribe to reduced motion preference
	prefersReducedMotion.subscribe((v) => (reducedMotion = v));

	onMount(async () => {
		if (!browser) return;

		// Dynamic imports for heavy dependencies
		const Lenis = (await import('lenis')).default;
		const gsap = (await import('gsap')).gsap;
		const { ScrollTrigger } = await import('gsap/ScrollTrigger');

		gsap.registerPlugin(ScrollTrigger);

		// Initialize Lenis (skip if reduced motion)
		let lenis: any = null;
		if (!reducedMotion) {
			lenis = new Lenis({
				lerp: 0.1,
				wheelMultiplier: 1,
				touchMultiplier: 2
			});

			setLenisInstance(lenis);

			// Sync Lenis with ScrollTrigger
			lenis.on('scroll', ScrollTrigger.update);
			gsap.ticker.add((time) => lenis.raf(time * 1000));
			gsap.ticker.lagSmoothing(0);
		}

		// Create scroll triggers for each section
		sections.forEach(({ id }) => {
			ScrollTrigger.create({
				trigger: `#${id}`,
				start: 'top center',
				end: 'bottom center',
				onEnter: () => {
					activeSection = id;
					currentSection.set(id);
				},
				onEnterBack: () => {
					activeSection = id;
					currentSection.set(id);
				}
			});
		});

		// Cleanup
		return () => {
			ScrollTrigger.getAll().forEach((t) => t.kill());
			lenis?.destroy();
		};
	});
</script>

<svelte:head>
	<title>Ethos — cix</title>
	<meta name="description" content="What we build and why, grounded in research. The evidence for collaborative intelligence." />
</svelte:head>

<main id="main" class="ethos">
	<ProgressNav {sections} currentSection={activeSection} />

	<!-- S1: The Productivity Illusion -->
	<ScrollySection id="illusion">
		<Step>
			<h1>Something is broken.</h1>
			<p class="lead">
				Not the outputs — the outputs look fine. The problem is underneath.
			</p>
		</Step>
		<Step>
			<DuelingStat
				leftValue={24}
				leftLabel="perceived faster"
				rightValue={19}
				rightLabel="measured slower"
				unit="%"
			/>
			<p class="paradox-note">
				METR ran a randomized controlled trial with 16 experienced developers
				on mature codebases. AI tools made them <strong>19% slower</strong>.
				They predicted being 24% faster.
			</p>
		</Step>
		<Step>
			<p>
				That 43-point perception gap isn't an anomaly. It's the cost of getting
				collaboration wrong. Developers feel faster but measure slower — and the gap
				between what people believe and what is true widens with each delegation.
			</p>
		</Step>
	</ScrollySection>

	<!-- S2: The Hollowing Problem -->
	<ScrollySection id="hollowing">
		<Step>
			<h2>The hollowing problem</h2>
			<p>The real cost isn't time. It's capability. Three things degrade with substitutive AI use:</p>
			<ol class="degradation-list">
				<li><strong>Skill to produce</strong> — you stop practicing</li>
				<li><strong>Judgment to evaluate</strong> — you can't assess what you didn't build</li>
				<li><strong>Metacognition to notice the loss</strong> — you can't feel yourself getting worse</li>
			</ol>
			<p>This is why the 43-point gap exists.</p>
		</Step>
		<Step>
			<ResearchTable>
				<table>
					<thead>
						<tr>
							<th>Finding</th>
							<th>Source</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td>~20% skill degradation in AI-assisted groups vs control</td>
							<td class="citation">Lee & Bastani, 2025</td>
						</tr>
						<tr>
							<td>Junior developers show greatest dependency effects</td>
							<td class="citation">Budzyń et al., 2025</td>
						</tr>
						<tr>
							<td>Metacognitive monitoring impaired after extended AI assistance</td>
							<td class="citation">Kosmyna et al., 2024</td>
						</tr>
						<tr>
							<td>Passive consumption predicts atrophy; active engagement does not</td>
							<td class="citation">Nature Human Behaviour, 2024</td>
						</tr>
					</tbody>
				</table>
			</ResearchTable>
		</Step>
		<Step>
			<p>
				This is not "humans get lazy." It's a feedback loop.
				Tool replaces thought. Human stops practicing. Human can't evaluate output.
				Human loses judgment. Dependency deepens.
			</p>
			<p>The loop is invisible from inside.</p>
		</Step>
	</ScrollySection>

	<!-- S3: Homogenization -->
	<ScrollySection id="homogenization">
		<Step>
			<h2>Homogenization</h2>
			<p>
				Given the same prompt, AI-assisted work converges toward identical outputs.
				Ten developers who would have produced ten architectures now produce one.
				Diversity of human perspective erodes into monoculture.
			</p>
		</Step>
		<Step>
			<ResearchTable>
				<table>
					<thead>
						<tr>
							<th>Finding</th>
							<th>Source</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td>AI-assisted solutions show significantly reduced variance across practitioners</td>
							<td class="citation">Convergent output analysis, multiple studies</td>
						</tr>
						<tr>
							<td>Competitive pressure selects for substitutive engagement patterns</td>
							<td class="citation">Organizational behavior research</td>
						</tr>
					</tbody>
				</table>
			</ResearchTable>
		</Step>
		<Step>
			<p>
				Market pressure locks this in. Teams that delegate fully ship faster this quarter.
				By the time fragility surfaces — brittle architectures, undetected failures,
				homogenized thinking — the atrophy is deep and the incentive structure
				rewards more of it.
			</p>
		</Step>
	</ScrollySection>

	<!-- S4: What Makes Collaboration Work -->
	<ScrollySection id="collaboration">
		<Step>
			<h2>What makes collaboration work</h2>
			<p>
				Blaurock et al. studied what factors predict successful human-AI collaboration.
				The results split cleanly.
			</p>
		</Step>
		<Step>
			<ResearchTable>
				<table>
					<thead>
						<tr>
							<th>Factor</th>
							<th>Effect</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td>Transparency of AI reasoning</td>
							<td class="positive">Positive predictor</td>
						</tr>
						<tr>
							<td>Human sense of control</td>
							<td class="positive">Positive predictor</td>
						</tr>
						<tr>
							<td>Reciprocity in interaction</td>
							<td class="positive">Positive predictor</td>
						</tr>
						<tr>
							<td>Engagement features (gamification, polish)</td>
							<td class="negative">Negative predictor</td>
						</tr>
						<tr>
							<td>AI anthropomorphization</td>
							<td class="negative">Negative predictor</td>
						</tr>
						<tr>
							<td>Ease of delegation (low friction to hand off)</td>
							<td class="negative">Negative predictor</td>
						</tr>
					</tbody>
				</table>
			</ResearchTable>
		</Step>
		<Step>
			<p>
				The features that make AI tools <em>feel</em> good — smooth UX, low friction,
				personality — predict worse outcomes. The features that make collaboration
				<em>work</em> — transparency, control, reciprocity — often feel like friction.
			</p>
			<p><strong>This is the design trap.</strong></p>
		</Step>
	</ScrollySection>

	<!-- S5: The Trust Paradox -->
	<ScrollySection id="trust">
		<Step>
			<h2>The trust paradox</h2>
			<p>The most counterintuitive finding. High use doesn't mean high trust.</p>
		</Step>
		<Step>
			<DuelingStat
				leftValue={84}
				leftLabel="use AI"
				rightValue={33}
				rightLabel="trust it"
			/>
			<p class="paradox-note">
				Most developers use AI despite not trusting it. Trust dropped from 43% to 33%
				even as adoption rose.
			</p>
		</Step>
		<Step>
			<p>
				This isn't irrational — it's strategic. Developers have learned that AI output
				requires verification but is still worth generating.
			</p>
			<div class="trust-comparison">
				<div class="trust-group">
					<span class="trust-label">Seniors</span>
					<span class="trust-stat warning">Low trust</span>
					<span class="trust-outcome success">Verify effectively, ship 2.5x more</span>
				</div>
				<div class="trust-group">
					<span class="trust-label">Juniors</span>
					<span class="trust-stat">Higher trust</span>
					<span class="trust-outcome warning">Lack skill base to know what to check</span>
				</div>
			</div>
		</Step>
	</ScrollySection>

	<!-- S6: Complementary vs Substitutive -->
	<ScrollySection id="complementary">
		<Step>
			<h2>Complementary vs substitutive</h2>
			<p>The same tool can operate in any of these modes depending on how it's designed:</p>
		</Step>
		<Step>
			<ResearchTable>
				<table>
					<thead>
						<tr>
							<th>Mode</th>
							<th>Description</th>
							<th>Outcome</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td><strong>Complementary</strong></td>
							<td>AI fills genuine gaps in human capability</td>
							<td class="positive">Human grows, system strengthens</td>
						</tr>
						<tr>
							<td><strong>Constitutive</strong></td>
							<td>AI and human form a new joint capability neither had alone</td>
							<td class="positive">Novel emergence, both essential</td>
						</tr>
						<tr>
							<td><strong>Substitutive</strong></td>
							<td>AI replaces human thought where human is capable</td>
							<td class="negative">Human atrophies, system degrades</td>
						</tr>
					</tbody>
				</table>
			</ResearchTable>
		</Step>
		<Step stat={{ value: 17, label: 'worse exam performance with unrestricted AI', source: 'Bastani PNAS 2025' }}>
			<p>
				Bastani's PNAS study: same AI, same students, different design.
				Unrestricted access caused 17% harm. Scaffolded access with guardrails
				caused no significant harm.
			</p>
			<p>The tool didn't change. The interaction pattern did.</p>
		</Step>
	</ScrollySection>

	<!-- S7: Cognitive Extensions -->
	<ScrollySection id="cognition">
		<Step>
			<h2>Cognitive extensions</h2>
			<p class="lead">Your notebook isn't just storage. It's part of how you think.</p>
		</Step>
		<Step>
			<p>
				Clark and Chalmers (1998) proposed the <strong>extended mind thesis</strong>:
				cognitive processes don't stop at the skull. If the notebook performs
				the same cognitive function as memory, it's part of the cognitive system.
			</p>
		</Step>
		<Step>
			<ExtendedMindDiagram />
		</Step>
		<Step>
			<p>
				Applied to AI: every extension in cix isn't a tool you use.
				It's part of the cognitive system the human-AI collaboration forms.
				The <em>design</em> of the extension shapes the <em>nature</em> of the mind.
			</p>
			<p class="the-question">
				The question isn't "is AI helpful?"<br />
				It's <strong>"what kind of mind are you building?"</strong>
			</p>
		</Step>
	</ScrollySection>

	<!-- S8: Design Constraints -->
	<ScrollySection id="constraints">
		<Step>
			<h2>Design constraints</h2>
			<p>
				Not what we believe — what we build and why. Four verifiable constraints,
				each grounded in research, each breaking a specific link in the atrophy loop.
			</p>
		</Step>
		<Step>
			<div class="atrophy-loop" aria-label="The atrophy loop: tool does work, human stops practicing, can't evaluate output, loses judgment, dependency deepens">
				<div class="loop-node">Tool does work</div>
				<div class="loop-arrow">&rarr;</div>
				<div class="loop-node">Human stops practicing</div>
				<div class="loop-arrow">&rarr;</div>
				<div class="loop-node">Can't evaluate output</div>
				<div class="loop-arrow">&rarr;</div>
				<div class="loop-node">Loses judgment</div>
				<div class="loop-arrow">&rarr;</div>
				<div class="loop-node">Dependency deepens</div>
				<div class="loop-return">&hookleftarrow;</div>
			</div>
		</Step>
		<Step>
			<div class="constraints-grid">
				<ConstraintCard
					name="Transparent by Design"
					description="Extensions expose reasoning, ship docs that teach domain knowledge, show decisions not just outputs."
					citation="Blaurock et al., 2025: transparency predicts good collaboration outcomes"
					loopBreaks="Breaks: can't evaluate output"
					verification="Does it log decisions? Do docs explain why, not just what?"
					delay={0}
				/>
				<ConstraintCard
					name="Evidence-Driven Design"
					description="Claims backed by data. Extensions prove they work. Build on prior work with attribution."
					citation="METR, 2025: 43-point perception gap exists because no one measured"
					loopBreaks="Breaks: the illusion that things are working"
					verification="Are claims supported? Is prior work cited? Can effectiveness be measured?"
					delay={150}
				/>
				<ConstraintCard
					name="Enable Diversity"
					description="Forkable, composable, multiple approaches coexist. No single blessed way."
					citation="Convergent output research: AI-assisted work converges toward identical solutions"
					loopBreaks="Breaks: tool does work one way forever"
					verification="Can it be forked? Do multiple approaches exist in the marketplace?"
					delay={300}
				/>
				<ConstraintCard
					name="Require Judgment"
					description="Extensions defer at decision points. Present choices instead of automating away expertise."
					citation="Lee & Bastani, 2025; Kosmyna et al., 2024: passive consumption predicts atrophy"
					loopBreaks="Breaks: dependency deepens"
					verification="Does it present choices where expertise matters? Does it defer to human judgment?"
					delay={450}
				/>
			</div>
		</Step>
	</ScrollySection>

	<!-- S9: The Goal -->
	<ScrollySection id="goal">
		<Step>
			<h2>The goal</h2>
			<blockquote>
				<p>Think with, not for.</p>
			</blockquote>
			<p>
				Every extension in cix is built to these constraints. Not because we believe
				in them abstractly, but because the research shows what happens when you don't.
			</p>
		</Step>
		<Step>
			<p class="cta">
				<a href="{base}/library">Explore the evidence &rarr;</a>
			</p>
		</Step>
	</ScrollySection>
</main>

<style>
	.ethos {
		background: var(--dao-bg);
	}

	h1 {
		font-size: var(--type-2xl);
		margin-bottom: var(--space-3);
	}

	.lead {
		font-size: var(--type-lg);
		color: var(--dao-text);
	}

	h2 {
		font-size: var(--type-xl);
		margin-bottom: var(--space-2);
	}

	table {
		margin: var(--space-2) 0;
	}

	.warning {
		color: var(--ci-red);
	}

	.success {
		color: var(--emergence-core);
	}

	/* Degradation List (S2) */
	.degradation-list {
		padding-left: var(--space-3);
		margin: var(--space-2) 0;
	}

	.degradation-list li {
		margin-bottom: var(--space-1);
	}

	/* Trust Paradox Styles */
	.paradox-note {
		font-size: var(--type-sm);
		color: var(--dao-muted);
		text-align: center;
		margin-top: var(--space-2);
	}

	.trust-comparison {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: var(--space-4);
		margin: var(--space-3) 0;
	}

	.trust-group {
		display: flex;
		flex-direction: column;
		gap: var(--space-1);
		padding: var(--space-2);
		background: var(--dao-surface);
		border-radius: var(--radius-sm);
	}

	.trust-label {
		font-family: var(--font-sans);
		font-size: var(--type-sm);
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: var(--tracking-wider);
		color: var(--dao-text);
	}

	.trust-stat {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
	}

	.trust-stat.warning {
		color: var(--ci-red);
	}

	.trust-outcome {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		padding-top: var(--space-1);
		border-top: 1px solid var(--dao-border);
	}

	.trust-outcome.success {
		color: var(--emergence-core);
	}

	.trust-outcome.warning {
		color: var(--ci-red);
	}

	/* Cognitive Extensions Styles */
	.the-question {
		font-size: var(--type-lg);
		text-align: center;
		margin-top: var(--space-4);
		padding: var(--space-3);
		background: var(--dao-surface);
		border-left: 4px solid var(--spark-core);
	}

	.the-question strong {
		color: var(--spark-core);
		display: block;
		font-size: var(--type-xl);
		margin-top: var(--space-1);
	}

	/* Atrophy Loop Diagram (S8) */
	.atrophy-loop {
		display: flex;
		align-items: center;
		flex-wrap: wrap;
		gap: var(--space-1);
		padding: var(--space-3);
		background: var(--dao-surface);
		border-radius: var(--radius-sm);
		margin: var(--space-2) 0;
	}

	.loop-node {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-text);
		padding: var(--space-0-5) var(--space-1);
		border: 1px solid var(--dao-border);
		border-radius: var(--radius-sm);
		white-space: nowrap;
	}

	.loop-arrow {
		color: var(--ci-red);
		font-size: var(--type-lg);
	}

	.loop-return {
		color: var(--ci-red);
		font-size: var(--type-xl);
		width: 100%;
		text-align: center;
		margin-top: var(--space-1);
	}

	/* Constraints Grid */
	.constraints-grid {
		display: grid;
		gap: var(--space-4);
	}

	blockquote {
		font-size: var(--type-lg);
		border-left-width: 4px;
		padding: var(--space-3);
		background: var(--dao-surface);
	}

	blockquote p {
		margin: 0;
		color: var(--dao-text);
	}

	.cta {
		margin-top: var(--space-4);
	}

	.cta a {
		font-family: var(--font-sans);
		font-size: var(--type-lg);
		font-weight: 600;
		color: var(--emergence-core);
		border-bottom-color: var(--emergence-core);
	}

	@media (max-width: 640px) {
		.trust-comparison {
			grid-template-columns: 1fr;
		}

		.atrophy-loop {
			flex-direction: column;
			align-items: stretch;
		}

		.loop-arrow {
			text-align: center;
			transform: rotate(90deg);
		}

		.loop-return {
			display: none;
		}
	}
</style>
