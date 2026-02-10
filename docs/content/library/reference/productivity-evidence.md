# Productivity Evidence

Research synthesis on AI-assisted developer productivity, code quality metrics, and security implications.

---

## Sources

- [Becker et al. (2025). Measuring AI Impact on Developer Productivity. METR.](https://arxiv.org/abs/2507.09089)
- [Cui/Demirer et al. (2024). Effects of Generative AI on High Skilled Work. RCTs.](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4671691)
- [GitClear (2025). Coding on Copilot: 2024 Data. Analysis of 211M LOC.](https://www.gitclear.com/coding_on_copilot_data_shows_ais_downward_pressure_on_code_quality)
- [Veracode (2025). State of Software Security: AI-Generated Code.](https://www.veracode.com/state-of-software-security-report)
- [Shukla et al. (2025). Security Implications of AI-Generated Code.](https://arxiv.org/abs/2501.03205)
- [Perry et al. (2025). Do Users Write More Insecure Code with AI Assistants?](https://arxiv.org/abs/2211.03622)
- [DORA (2024). Accelerate State of DevOps Report.](https://cloud.google.com/devops/state-of-devops)
- [Stack Overflow Developer Survey (2024-2025).](https://survey.stackoverflow.co/2024/)

---

## The Perception Gap

### METR RCT (2025) <span class="ev ev-moderate" title="RCT, n=16, within-subject design on own repos">◐</span>

**Design:** Within-subject RCT. 16 experienced open-source developers working in their own repositories on real tasks from their backlogs.

**Key findings:**

| Metric | Without AI | With AI | Gap |
|--------|-----------|---------|-----|
| Actual completion time | Baseline | **+19% slower** | -19% |
| Predicted completion time | Baseline | -24% faster | **+43 points** |
| Developer confidence | — | "AI made me faster" | Illusion |

The miscalibration is structural. Time spent prompting, reviewing suggestions, fixing integration issues, and context-switching doesn't register as "work." Code appearing on screen feels like productivity. The invisible effort of verification and correction disappears from perception.

**Why this study matters:** No toy problems, no unfamiliar domains, no confounding variables. Experienced developers in codebases they knew best. The most controlled productivity measurement available.

**Limitations:** n=16 — rigorous design but small sample. Experienced developers only (no juniors). Short-term tasks.

### Perception at Scale

Stack Overflow survey data confirms the trap:

| Metric | 2024 | 2025 | Direction |
|--------|------|------|-----------|
| AI adoption | 76% | 84% | Rising |
| Trust in AI accuracy | 43% | 33% | Falling |

Adoption rises while trust falls. People use tools they don't trust because perceived productivity overrides measured performance.

---

## Productivity Gains (Real)

### Cui/Demirer RCTs (2024) <span class="ev ev-strong" title="Multiple RCTs, n=4,867">●</span>

**Design:** Multiple randomized controlled trials across high-skilled occupations. Total n=4,867.

**Key finding:** 26% more tasks completed with AI assistance.

The productivity gains are real and substantial. This isn't contested. The question is whether they come at the cost of capability development — and the evidence from [skill formation →](skill-formation-evidence) suggests the tradeoff is engagement-pattern-dependent.

### What Actually Improves

| Task Type | Evidence | Magnitude |
|-----------|----------|-----------|
| Boilerplate generation | Multiple studies | Significant time savings |
| Code translation | GitHub research | Meaningful improvement |
| API exploration | Microsoft research | Faster onboarding |
| Prototyping | Surveys + anecdotal | Widely reported |

Gains concentrate in generation-heavy tasks with low maintenance burden.

---

## Code Quality Degradation

### GitClear (2025) <span class="ev ev-strong" title="Longitudinal analysis, 211M LOC across organizations">●</span>

**Design:** Analysis of 211 million lines of code across organizations before and after AI adoption.

**Key findings:**

| Metric | Before AI | After AI |
|--------|-----------|----------|
| Code duplication rate | Baseline | **8x increase** |
| Refactoring commits | Baseline | **Sharp decline** |
| "Moved" and "Copy/paste" code | Baseline | **Significant increase** |

**Mechanism:** AI generates code without awareness of existing implementations. Each generation produces a fresh solution. The developer who would have searched for reusable components instead gets plausible new code — faster to accept than to find and integrate.

**The cathedral-to-prefabs shift:** Codebases transition from designed (developer architected) to assembled (connected generated components). Refactoring decline signals loss of abstraction skill.

### DORA Metrics (2024) <span class="ev ev-strong" title="Industry survey, large sample">●</span>

Industry-wide engineering effectiveness:

| Metric | Change with AI adoption |
|--------|-------------------------|
| Deployment stability | **-7.2%** |
| Throughput | **-1.5%** |

Not one company or team — the aggregate signal across the industry. AI adoption correlates with slight degradation in metrics that matter for software delivery performance.

---

## Security Degradation

### Baseline Vulnerability Rate

**Veracode (2025):** 45% of AI-generated code contains critical vulnerabilities. <span class="ev ev-moderate" title="Veracode static analysis report">◐</span> Basic patterns: hardcoded credentials, SQL injection via string concatenation, missing input validation, insecure deserialization.

### The Iteration Trap

**Shukla et al. (2025):** Security degrades with iteration, not improves. <span class="ev ev-moderate" title="Shukla et al. arXiv, systematic analysis">◐</span>

| Iteration | Vulnerabilities per 1000 LOC |
|-----------|------------------------------|
| Initial generation | 2.1 |
| After refinement | **6.2** |

Each round adds code without removing vulnerabilities from previous rounds. The human reviewing iteration N has more to verify and less understanding of cumulative risk.

### Vulnerability Inheritance

**Perry et al. (2025):** Analysis of 7,703 files. AI inherits vulnerabilities from training data systematically. <span class="ev ev-moderate" title="Perry et al. arXiv, 7,703 file analysis">◐</span> When Stack Overflow is training corpus and Stack Overflow contains insecure patterns, AI reproduces them faithfully. The model has no concept of "this pattern is insecure" — only "this pattern is common."

Model size provides no protection. Larger models aren't more secure.

---

## The Explainability Gap

Code complexity increases while developer understanding decreases. A compounding pattern:

```
Sprint 1: Developer writes 500 LOC, understands all of it
Sprint 2: AI generates 2000 LOC, developer understands ~60%
Sprint 3: AI generates atop Sprint 2, developer understands ~30%
Sprint N: Codebase assembled, not designed — comprehension lost
```

Consequences:
- Can't debug what you don't understand
- Can't maintain what you can't reason about
- Can't secure code you haven't comprehended
- Can't evolve architecture you didn't design

The productivity gain in generation becomes productivity loss in maintenance.

---

## Evidence Summary

| Finding | Effect Size | Evidence Level | Source |
|---------|------------|----------------|--------|
| Perception gap: predicted vs actual | 43 percentage points | <span class="ev ev-moderate">◐</span> Moderate | METR RCT 2025 |
| Task completion gains | +26% more tasks | <span class="ev ev-strong">●</span> Strong | Cui/Demirer RCTs |
| Code duplication increase | 8x | <span class="ev ev-strong">●</span> Strong | GitClear, 211M LOC |
| Deployment stability decline | -7.2% | <span class="ev ev-strong">●</span> Strong | DORA 2024 |
| Critical vulnerability rate | 45% | <span class="ev ev-moderate">◐</span> Moderate | Veracode 2025 |
| Security degrades with iteration | 2.1 → 6.2 vuln/KLOC | <span class="ev ev-moderate">◐</span> Moderate | Shukla 2025 |
| Trust-adoption divergence | Trust -10pp, adoption +8pp | <span class="ev ev-moderate">◐</span> Moderate | Stack Overflow |

---

*Full citations in [bibliography](bibliography)*
