<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { browser } from '$app/environment';
	import ScrollySection from '$lib/components/ethos/ScrollySection.svelte';
	import Step from '$lib/components/ethos/Step.svelte';
	import ProgressNav from '$lib/components/ethos/ProgressNav.svelte';
	import { GlyphBackground } from '$lib/components/atmosphere';
	import { setLenisInstance, prefersReducedMotion, currentSection } from '$lib/stores/scroll';

	// Section definitions
	const sections = [
		{ id: 'intro', title: 'Why This Approach' },
		{ id: 'illusion', title: 'The Productivity Illusion' },
		{ id: 'hollowing', title: 'The Hollowing Problem' },
		{ id: 'collaboration', title: 'What Makes Collaboration Work' },
		{ id: 'complementary', title: 'Complementary vs Substitutive' },
		{ id: 'principles', title: 'Core Principles' },
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

	<!-- Core Principles -->
	<ScrollySection id="principles">
		<Step>
			<h2>Core principles</h2>
			<p>From the research:</p>
		</Step>
		<Step>
			<dl class="principles">
				<dt>Complementary</dt>
				<dd>AI amplifies, doesn't replace. Human remains central.</dd>

				<dt>Constitutive</dt>
				<dd>Enables new capability through collaboration. The whole is other than the sum of its parts.</dd>

				<dt>Transparent by default</dt>
				<dd>Provenance, traceability, explanations, observability. Show reasoning at every step.</dd>

				<dt>Compounding mastery</dt>
				<dd>Each interaction makes both human and AI more capable. Learning compounds.</dd>

				<dt>Enabling control</dt>
				<dd>User agency is the strongest lever (β = 0.507). Shape how, not just what.</dd>

				<dt>Non-conformity</dt>
				<dd>Preserve intellectual diversity. Resist homogenization. Different perspectives enable collective intelligence.</dd>
			</dl>
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
		color: var(--dao-red);
	}

	.success {
		color: var(--dao-green);
	}

	.principles {
		display: grid;
		gap: var(--space-2);
	}

	.principles dt {
		font-family: var(--font-sans);
		font-weight: 600;
		color: var(--dao-blue);
		margin-bottom: var(--space-1);
	}

	.principles dd {
		margin: 0 0 var(--space-2) 0;
		padding-left: var(--space-2);
		border-left: 2px solid var(--dao-border);
		color: var(--dao-muted);
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
		color: var(--dao-green);
		border-bottom-color: var(--dao-green);
	}
</style>
