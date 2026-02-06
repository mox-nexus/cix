<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { browser } from '$app/environment';
	import ScrollySection from '$lib/components/ethos/ScrollySection.svelte';
	import Step from '$lib/components/ethos/Step.svelte';
	import ProgressNav from '$lib/components/ethos/ProgressNav.svelte';
	import DuelingStat from '$lib/components/ethos/DuelingStat.svelte';
	import ExtendedMindDiagram from '$lib/components/ethos/ExtendedMindDiagram.svelte';
	import PrincipleCard from '$lib/components/ethos/PrincipleCard.svelte';
	import { GlyphBackground } from '$lib/components/atmosphere';
	import { setLenisInstance, prefersReducedMotion, currentSection } from '$lib/stores/scroll';

	// Section definitions
	const sections = [
		{ id: 'intro', title: 'Why This Approach' },
		{ id: 'illusion', title: 'The Productivity Illusion' },
		{ id: 'hollowing', title: 'The Hollowing Problem' },
		{ id: 'collaboration', title: 'What Makes Collaboration Work' },
		{ id: 'trust', title: 'The Trust Paradox' },
		{ id: 'complementary', title: 'Complementary vs Substitutive' },
		{ id: 'cognition', title: 'Cognitive Extensions' },
		{ id: 'principles', title: 'Design Principles' },
		{ id: 'goal', title: 'The Goal' }
	];

	let activeSection = $state<string | null>('intro');
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
	<title>Why This Approach — cix</title>
	<meta name="description" content="Understanding what makes AI collaboration go wrong — and what makes it go right." />
</svelte:head>

<GlyphBackground>
<main id="main" class="ethos">
	<ProgressNav {sections} currentSection={activeSection} />

	<!-- Intro -->
	<ScrollySection id="intro">
		<Step>
			<h1>We build together.</h1>
			<p class="lead">
				Not master and servant. Not tool and user. <strong>Collaborators.</strong>
			</p>
			<p>
				METR ran a randomized controlled trial with 16 experienced developers on mature codebases.
				AI tools made them <strong>19% slower</strong>. They predicted being 24% faster.
			</p>
			<p>
				That 43-point perception gap isn't an anomaly. It's the cost of getting collaboration wrong.
			</p>
		</Step>
	</ScrollySection>

	<!-- The Productivity Illusion -->
	<ScrollySection id="illusion">
		<Step>
			<h2>The productivity illusion</h2>
			<p>Developers believe AI helps. Measurements say otherwise.</p>
			<p>
				Trust in AI coding accuracy dropped from 43% to 33% in one year (Stack Overflow 2024-2025).
				Adoption rose to 84% over the same period. People use tools they don't trust,
				perceive benefits they don't get.
			</p>
		</Step>
		<Step>
			<p>The illusion has a mechanism.</p>
			<p>
				AI shifts work from generation to verification. Coding feels easier because writing
				from scratch is gone. But catching subtle errors in mostly-correct code takes longer
				and demands sustained attention.
			</p>
		</Step>
		<Step stat={{ value: 30, label: 'of seniors edit AI output enough to offset time savings', source: 'vs 17% of juniors' }}>
			<p>
				Seniors ship 2.5x more AI code to production despite lower trust.
				They can verify; juniors can't.
			</p>
		</Step>
	</ScrollySection>

	<!-- The Hollowing Problem -->
	<ScrollySection id="hollowing">
		<Step>
			<h2>The hollowing problem</h2>
			<p>Beyond productivity, there's capability.</p>
		</Step>
		<Step>
			<table>
				<thead>
					<tr>
						<th>Study</th>
						<th>Finding</th>
						<th>Timeframe</th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td>Lee CHI 2025</td>
						<td>Higher AI confidence → less critical thinking</td>
						<td>Cross-sectional</td>
					</tr>
					<tr>
						<td>Budzyń Lancet 2025</td>
						<td>20% skill degradation after AI removal</td>
						<td>3 months</td>
					</tr>
					<tr>
						<td>Kosmyna MIT 2025</td>
						<td>83% couldn't recall AI-assisted content</td>
						<td>Immediate</td>
					</tr>
					<tr>
						<td>Bastani PNAS 2025</td>
						<td>Unrestricted AI → 17% worse exam performance</td>
						<td>Single course</td>
					</tr>
				</tbody>
			</table>
		</Step>
		<Step stat={{ value: 20, label: 'skill degradation after 3 months', source: 'Budzyń Lancet 2025' }}>
			<p>
				The Budzyń study is clearest. Endoscopists used AI-assisted polyp detection for 3 months.
				When removed, their detection rate had dropped from 28.4% to 22.4%. The skill atrophied measurably.
			</p>
			<p>
				No equivalent study exists for developers — the technology is too new.
				But the cognitive mechanisms are the same. You don't maintain skills you stop exercising.
			</p>
		</Step>
	</ScrollySection>

	<!-- What Makes Collaboration Work -->
	<ScrollySection id="collaboration">
		<Step>
			<h2>What makes collaboration work</h2>
			<p>
				Blaurock et al. (Journal of Service Research, 2024) studied collaborative intelligence
				through interviews and experiments with 654 professionals. What predicted good outcomes:
			</p>
		</Step>
		<Step>
			<table>
				<thead>
					<tr>
						<th>Factor</th>
						<th>Effect</th>
						<th>What it means</th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td>Transparency</td>
						<td>Strong positive</td>
						<td>User sees AI reasoning → better outcomes</td>
					</tr>
					<tr>
						<td>Process control</td>
						<td>Strongest positive</td>
						<td>User shapes how AI works → better outcomes</td>
					</tr>
					<tr>
						<td>Outcome control</td>
						<td>Strong positive</td>
						<td>User shapes what AI produces → better outcomes</td>
					</tr>
					<tr>
						<td>Reciprocity</td>
						<td>Strong positive</td>
						<td>User grows through collaboration → better outcomes</td>
					</tr>
					<tr>
						<td>Engagement features</td>
						<td class="warning">Significant negative</td>
						<td>AI asks questions → worse for frequent users</td>
					</tr>
				</tbody>
			</table>
		</Step>
		<Step>
			<p>
				The engagement finding surprised people. Making AI conversational was supposed to build trust.
				Instead, for frequent users, engagement features significantly hurt perceived quality.
			</p>
			<p><strong>The pattern:</strong> showing reasoning and giving control work. Prompting for interaction doesn't.</p>
		</Step>
	</ScrollySection>

	<!-- The Trust Paradox -->
	<ScrollySection id="trust">
		<Step>
			<h2>The trust paradox</h2>
			<p>The numbers don't add up — until they do.</p>
		</Step>
		<Step>
			<DuelingStat
				leftValue={84}
				leftLabel="use AI"
				rightValue={33}
				rightLabel="trust it"
			/>
			<p class="paradox-note">
				46% actively distrust. Only 60% view AI favorably, down from 77% in 2023.
				People adopt tools they don't believe in.
			</p>
		</Step>
		<Step>
			<p>The paradox resolves when you look at who ships.</p>
			<div class="trust-comparison">
				<div class="trust-group">
					<span class="trust-label">Seniors</span>
					<span class="trust-stat warning">20% high distrust</span>
					<span class="trust-outcome success">Ship 2.5x more AI code</span>
				</div>
				<div class="trust-group">
					<span class="trust-label">Juniors</span>
					<span class="trust-stat">17% rely without editing</span>
					<span class="trust-outcome warning">Can't verify, can't catch errors</span>
				</div>
			</div>
			<p>
				<strong>Low trust enables high output.</strong> Seniors treat AI as rough draft material —
				fast generation, heavy revision. The productivity comes from rapid correction, not AI correctness.
			</p>
		</Step>
		<Step>
			<p>
				Explanations don't fix miscalibrated trust. Bansal et al. (CHI 2021) found that
				detailed AI explanations <em>increase</em> overreliance.
			</p>
			<p>
				What works: cognitive forcing functions. Requiring engagement before accepting output.
				It improves calibration but hurts satisfaction.
				<strong>The interventions that work aren't the ones people like.</strong>
			</p>
		</Step>
	</ScrollySection>

	<!-- Complementary vs Substitutive -->
	<ScrollySection id="complementary">
		<Step>
			<h2>Complementary vs substitutive</h2>
			<p>AI can extend capability three ways:</p>
		</Step>
		<Step>
			<table>
				<thead>
					<tr>
						<th>Type</th>
						<th>Human role</th>
						<th>Outcome</th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td><strong>Complementary</strong></td>
						<td>Learns, guides, improves</td>
						<td class="success">Better with and without AI</td>
					</tr>
					<tr>
						<td><strong>Constitutive</strong></td>
						<td>Enables capability impossible alone</td>
						<td class="success">New capability emerges</td>
					</tr>
					<tr>
						<td><strong>Substitutive</strong></td>
						<td>Passively consumes output</td>
						<td class="warning">Skills atrophy</td>
					</tr>
				</tbody>
			</table>
		</Step>
		<Step stat={{ value: 17, label: 'worse exam performance with unrestricted AI', source: 'Bastani PNAS 2025' }}>
			<p>
				Bastani's PNAS study makes this concrete. Same AI, same students, different design:
			</p>
			<ul>
				<li>Unrestricted access: -17% exam performance</li>
				<li>Scaffolded access with guardrails: no significant harm</li>
			</ul>
			<p>The tool didn't change. The interaction pattern did.</p>
		</Step>
	</ScrollySection>

	<!-- Cognitive Extensions -->
	<ScrollySection id="cognition">
		<Step>
			<h2>Cognitive extensions</h2>
			<p class="lead">Your notebook isn't just storage. It's part of how you think.</p>
		</Step>
		<Step>
			<p>
				Clark and Chalmers (1998) proposed the <strong>extended mind thesis</strong>:
				cognitive processes don't stop at the skull.
			</p>
			<p>
				Otto uses a notebook to remember the museum address. Inga uses biological memory.
				Philosophy of mind says: if we call Inga's process "remembering,"
				we should call Otto's the same. <em>The notebook is part of Otto's mind.</em>
			</p>
		</Step>
		<Step>
			<ExtendedMindDiagram />
		</Step>
		<Step>
			<p>
				<strong>The parity principle:</strong> if a process were done in the head,
				we'd call it cognition. When external but functionally equivalent, it's cognitive extension.
			</p>
			<p>
				This is why we call them cognitive extensions, not tools.
				They become part of how you think.
			</p>
			<p class="the-question">
				The question isn't "is AI helpful?"<br />
				It's <strong>"what kind of mind are you building?"</strong>
			</p>
		</Step>
	</ScrollySection>

	<!-- Design Principles -->
	<ScrollySection id="principles">
		<Step>
			<h2>Design principles</h2>
			<p>From the research, four principles for extension design:</p>
		</Step>
		<Step>
			<div class="principles-grid">
				<PrincipleCard
					name="Collaborative Agency"
					description="Both human and AI retain agency. Transparency requires AI that shows its work. Control requires AI that can be directed. Neither master nor servant — collaborators."
					accent="blue"
					delay={0}
				/>
				<PrincipleCard
					name="Bidirectional Learning"
					description="The human learns, not just consumes. Reciprocity predicts good outcomes. Passive consumption predicts atrophy. Each interaction should make you more capable."
					accent="green"
					delay={150}
				/>
				<PrincipleCard
					name="Transparent Abstractions"
					description="Extensions should be readable, forkable, verifiable. If you can't see through it, you can't learn from it. Black boxes don't build trust."
					accent="neutral"
					delay={300}
				/>
				<PrincipleCard
					name="Compounding Engineering"
					description="Each solution makes the next one faster. Write it down, build on it. Mastery compounds with every use."
					accent="green"
					delay={450}
				/>
			</div>
		</Step>
	</ScrollySection>

	<!-- The Goal -->
	<ScrollySection id="goal">
		<Step>
			<h2>The goal</h2>
			<blockquote>
				<p>You're not done when it works. You're done when it's right.</p>
			</blockquote>
			<p>
				An extension succeeds when the human is better at the domain after using it.
				An extension fails when the human can't function without it.
			</p>
			<p>
				I'm not here to think for you. I'm here to think <em>with</em> you.
			</p>
		</Step>
		<Step>
			<p class="cta">
				<a href="/library">Explore the evidence →</a>
			</p>
		</Step>
	</ScrollySection>
</main>
</GlyphBackground>

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

	/* Principles Grid */
	.principles-grid {
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
	}
</style>
