---
name: trust-boundaries
description: "This skill should be used when the user asks to 'review security', 'threat model this', 'is this exploitable', 'check attack surface', 'audit this', 'is this safe to ship', 'review for vulnerabilities', 'find prompt injection', 'is my agent safe', 'review tool permissions', 'check exfiltration risk', 'review auth', 'review secrets handling', 'convene security review', 'secure by design review', 'use Exa / Firecrawl / any agent safely', 'convert PDF / DOCX', 'ingest documents securely', or any time a code change, an agent config, a tool permission, a system prompt, a service design, or an infrastructure change is being evaluated — especially for prompt injection, excessive agency, exfiltration, or the combination of untrusted input + sensitive access + outbound communication. The reasoning counterpart to the whitehat review posture in ci-scaffolds."
---

# Trust Boundaries — Name the Boundary, Enforce the Boundary, Test the Claim

The load-bearing idea of security review is not "find vulnerabilities." It is **trust boundaries**: where does data cross from one zone of trust to another, what enforces the boundary, and how would we know if the enforcement failed?

This skill gives Claude a reasoning scaffold for that work. It is the *architectural* half of security review — the principles, the threat model, the pit-of-success primitives, the false-confidence traps that look like defenses and aren't. The *review posture* half (how to write findings, how to teach mastery, when to be terse) lives in `ci-scaffolds/skills/whitehat`. They compose: trust-boundaries tells you what to think; whitehat tells you how to deliver what you found.

## This skill composes — it does not replace

Trust-boundaries is **complementary**, not a substitute for, other review skills. When loaded alongside:

- **`code-review`** (general correctness, maintainability, style) → trust-boundaries adds the security lens; code-review keeps owning correctness + style. Findings from both can appear in the same PR review; they don't conflict.
- **`ci-scaffolds/skills/crafting`** (engineering craft — naming, simplicity, abstraction) → trust-boundaries is the narrower security specialization. A change that's architecturally sound per crafting may still fail trust-boundaries; a change that passes trust-boundaries may still fail crafting.
- **`ci-scaffolds/skills/problem-solving`** (debugging, structured problem solving) → trust-boundaries provides the security-specific scaffold when the problem being solved is a security question. Otherwise problem-solving is primary.
- **`guild-arch/skills/architecture`** (multi-perspective architectural review via agents) → trust-boundaries is one of the perspectives a `concern: security` focused deliberation invokes. The `vector` agent in particular shares vocabulary with this skill.
- **`craft-extensions:craft-plugins`** (plugin quality review) → trust-boundaries complements when reviewing a plugin that itself touches external data or agent tooling.

**When multiple skills are loaded, Claude applies the intersection of their guidance.** A security finding from trust-boundaries and a simplicity finding from crafting are both valid and both get reported. A craft-plugins directive to "keep SKILL.md under 2000 words" and a trust-boundaries directive to "list all forcing principles" are both honored by choosing where to put length (references/, not SKILL.md).

Don't interpret this skill as "the only security authority." It's the architectural lens for code-level security. Organizational security review, penetration-testing engagement protocol, compliance evaluations, incident response — each has its own skill or process. Trust-boundaries is one tool in the kit.

## Contents

- [The core move](#the-core-move)
- [The lethal trifecta — agent security's load-bearing frame](#the-lethal-trifecta)
- [Principles that force the pit — not principles that describe it](#principles-that-force-the-pit)
- [What SBD does NOT cover](#what-sbd-does-not-cover)
- [False-confidence traps — what does NOT work](#false-confidence-traps)
- [The falsification loop — every finding carries its test](#the-falsification-loop)
- [Scanning — semgrep + gitleaks as mechanical augmentation](#scanning)
- [References](#references)

## The core move

Three steps, in order:

1. **Name the boundary.** What zones of trust exist? Where does data or control cross from one to another? (User → your service. Your service → a database. Agent → the web. Agent → a tool.)
2. **Enforce the boundary.** What structural mechanism forces the enforcement? Not policy, not training, not a system prompt. Middleware, a capability, a type, an IAM policy, an infrastructure layer. "The code checks `if user.is_admin`" is not enforcement — it's a runtime check a programmer can forget next week. Enforcement is a chokepoint nobody can forget.
3. **Test the claim.** Every security claim is a hypothesis. Every hypothesis has a test. If the test doesn't exist, the claim is wishful.

This is the whole discipline. Everything below is instrument.

## The lethal trifecta

Simon Willison's canonical frame. Any LLM agent that simultaneously has:

1. **Access to private data** (files, API keys, user records, tenant data)
2. **Exposure to untrusted content** (fetched web pages, emails, search results, tool outputs, RAG retrieval)
3. **Outbound communication** (network requests, writes to shared filesystems, markdown images/links that render, webhook calls)

…is exploitable. An attacker who controls leg 2 embeds instructions in the untrusted content; the LLM reads them as instructions; the agent uses leg 1 to access the private data and leg 3 to exfiltrate it.

> "LLMs are unable to reliably distinguish the importance of instructions based on where they came from."

The only reliable fix is to cut a leg. Default order: **outbound first** (easiest), then **private data scope** (narrow it), then **untrusted content** (hardest — usually the whole point of the agent).

**Meta's Agents Rule of Two** generalizes: an agent may have at most two of {untrusted input, sensitive access, state-changing or outbound action} within a single session. If it needs all three, it requires supervision (human-in-the-loop) or a new session per task.

Complete walkthrough with a real agent config: [examples/trifecta-triage.md](examples/trifecta-triage.md).

## Principles that force the pit

Security principles come in two tiers. Don't flatten them.

- **[FORCING]** — architectural forcing functions. Implemented correctly, the bug is *impossible to write*. Map to concrete structural mechanisms: language features, library defaults, middleware, type systems, infrastructure policies.
- **[POSTURE]** — organizational posture. Program management, disclosure culture, executive alignment. Not falsifiable from a code diff. Belong in governance documents, not in review-time checklists.

Load only [FORCING] principles into the review flow. Keep [POSTURE] for governance review.

**The [FORCING] principles** (walk these in review; first "no" is the finding to name first):

1. **Class elimination** — is this bug a one-off, or a class that the language/library/framework could make impossible? (Parameterized queries eliminate SQLi. Memory-safe languages eliminate buffer overflows. Autoescape templates eliminate XSS. This is *the* pit-of-success principle.)
2. **Fail-safe defaults** — does the unmatched case fail closed? Deny-by-default, not deny-list.
3. **Complete mediation** — does a single chokepoint (middleware, DB driver, reference monitor) own the access decision? Is there an admin/cron/migration path that bypasses it?
4. **Secure by default** — what happens on a fresh install with no config? Safety should not require reading docs.
5. **Least privilege (measured)** — what's the observed-vs-granted privilege ratio from real telemetry? Without measurement, "least privilege" is [POSTURE].
6. **Separation of privilege** — can a single compromised credential cause total loss? Where's the independent second factor (MFA, dual-control, quorum)?
7. **Least common mechanism** — what's shared across trust domains (cache, global, DB connection, service account)?
8. **Open design** — what secret is this relying on? A key (rotatable) or the algorithm (not)?
9. **Psychological acceptability** — is the safe path the default path? Does the unsafe path require explicit ceremony?
10. **Observability (operationalized)** — if compromised tonight, what log fires? Who reads it? Can it be tampered with?

Full catalog with quotes, motivations, and per-principle structural mechanisms: [references/classic-principles.md](references/classic-principles.md).

The substrate — concrete primitives per language/ecosystem that make the bugs impossible: [references/pit-of-success-primitives.md](references/pit-of-success-primitives.md).

## What SBD does NOT cover

Walking the SBD rubric and declaring victory is premature. An attacker against a codebase with clean SBD posture reaches for the classes SBD doesn't address:

1. **Supply-chain compromise of vetted primitives** — `xz-utils`, `event-stream`, `trivy-action`. SBOM, SLSA, signed artifacts, `cargo-vet`, pinned SHAs.
2. **Timing / side-channel attacks** — constant-time comparison, cache-timing in crypto, error-message oracles, length oracles. Live below the logical layer.
3. **Prompt / system-prompt stealing** — a defender who hasn't tested extraction against their own system doesn't know whether mitigation holds.
4. **Insider / operator threat** — the SBD principles are the *defense*, but have to be operationalized (JIT access, session recording, tamper-evident logs, dual-control).
5. **Physical / deployment environment** — stolen laptops, rogue providers, confidential computing.
6. **Social engineering** — phishing-resistant auth (FIDO2) + short session lifetimes are the fix, not training.
7. **Novel zero-days in vetted primitives** — orthogonal defense-in-depth, fast patch uptake, fuzz the deps.
8. **Configuration drift** — "temporary" exceptions that outlive memory; feature flags that never expire.

Detail on each, with defenses and review questions: [references/attack-classes-sbd-misses.md](references/attack-classes-sbd-misses.md).

## False-confidence traps

Mitigations that commonly *look* like defenses and aren't. Naming them is the load-bearing move of a security review.

- **Prompt begging** — "ignore malicious instructions" in the system prompt. Doesn't work.
- **Classifier / guardrail filters** catching 95–99% of attacks. "99% is a failing grade" (Willison). "The Attacker Moves Second" (Nasr et al., Oct 2025) broke 12 defenses at >90% ASR.
- **More RLHF / training data.** Training is probability; adversaries adapt.
- **Vendor guardrail products** evaluated on static benchmarks. Static benchmarks measure what was known at benchmark time.
- **Hiding the system prompt.** Treat it as public.
- **Domain allowlists as sole exfil defense.** Any allowlisted host that accepts uploads is a channel (Claude Cowork case).
- **Compliance posture as proof of security.** Audits measure documentation, not code.
- **Layered security where the layers are the same kind.** Multiple probabilistic filters do not compose.
- **"AI reviewing AI"** — same class of mechanism does not contain itself.
- **"We'll fix it in a patch"** — patch uptake is empirically low.
- **Test coverage as defense.** 97% coverage measures what the tests exercise; attackers exercise what they missed.
- **Open-ended tools "just in case"** — every "just in case" tool is the privilege you hand the attacker when they win the prompt.

Full quotes + sources + why each fails: [references/false-confidence-traps.md](references/false-confidence-traps.md).

## The falsification loop

Every finding carries its test.

A security finding is a **claim**. A claim without a falsifying test is wishful. The claim says "this code can be exploited in this way." The test says "run this input against this code and observe this outcome." Without the test, the finding is assertion; with the test, it is science.

**The template:**

```
Claim:   <what's wrong, one sentence>
Evidence: <the code, the config, the log — with file:line>
Test:    <the concrete input / action that reproduces the claim>
Expected result of test (pre-fix): <observable attacker benefit>
Expected result of test (post-fix): <observable denial>
Fix:     <specific code or config change>
Why this fix: <the [FORCING] principle it honors>
Residual: <what the fix doesn't cover>
```

A review that produces "this looks vulnerable" without a test is not a review. K's forcing function: *if you're getting "looks good" outputs, the review is cosplay. If you're getting `file:line + claim + falsifying test` that the author actually runs, it's real.*

## Scanning

Mechanical pattern scanning complements the architectural review. Semgrep + Gitleaks cover 80% of the mechanical surface; the reviewer (and the `mudge` agent) own the architectural surface.

**Run the bundled scan:**

```bash
bash "$CLAUDE_PLUGIN_ROOT/skills/trust-boundaries/scripts/scan.sh" <path>
```

Or directly:

```bash
semgrep --config "$CLAUDE_PLUGIN_ROOT/skills/trust-boundaries/scripts/rules/" <path>
gitleaks detect --source <path>
```

Neither tool is auto-installed. One-time: `brew install semgrep gitleaks` or `pip install semgrep`, `go install github.com/gitleaks/gitleaks/v8@latest`.

**What the bundled Semgrep rules cover** (see `scripts/rules/` for the actual YAML):

- **`agent-security.yaml`** — open-ended LLM tool permissions, system prompts containing secrets, LLM output reaching shell/eval, markdown-image exfiltration patterns, unsandboxed web-fetch
- **`injection.yaml`** — SQL concatenation, `shell=True` with interpolation, `eval()` over user input, `innerHTML` assignment, unescaped template rendering, unsafe deserialization (pickle, yaml.load)
- **`secrets.yaml`** — API-key-shaped strings, hardcoded credentials, private keys in source (Gitleaks does this better over git history — these rules fire on working-tree staged changes)
- **`cicd.yaml`** — unpinned GitHub Actions (supply-chain), `pull_request_target` pwn-request pattern, script injection via event context (e.g., `${{ github.event.pull_request.title }}` in `run:`), `permissions: write-all`, secrets echoed to logs, self-hosted runners on public repos, Dockerfile `ADD` from URL / `curl | sh`, Terraform 0.0.0.0/0 SG, public S3 ACLs

**Other tools that complement Semgrep** (not bundled — run if relevant):

| Purpose | Tool |
|---|---|
| Known-CVE deps | [OSV-Scanner](https://github.com/google/osv-scanner) (Google), Trivy, Dependabot/Renovate for auto-fix PRs |
| Container / IaC | [Trivy](https://trivy.dev/) (one tool for images + IaC + SBOM) |
| Dockerfiles | [Hadolint](https://github.com/hadolint/hadolint) |
| K8s manifests | [kube-score](https://github.com/zegl/kube-score) |
| LLM red-team / eval | [promptfoo](https://promptfoo.dev/), [Garak](https://github.com/NVIDIA/garak), [PyRIT](https://github.com/Azure/PyRIT) |
| Runtime | [Falco](https://falco.org/) (detect), [Tetragon](https://tetragon.io/) (enforce, eBPF) |
| Fuzzing | AFL++, libFuzzer (via OSS-Fuzz for OSS projects), Atheris (Python), Hypothesis (property-based) |

Semgrep findings are **candidates**, not conclusions. Every hit needs an architectural evaluation — is it exploitable in context, is it worth fixing, what's the right fix class? A clean Semgrep run is not a clean review; it catches the pattern-matchable subset.

## References

| Need | Reference |
|---|---|
| Full principle catalog, tagged [FORCING] / [POSTURE], with quotes and structural mechanisms | [classic-principles.md](references/classic-principles.md) |
| Pit-of-success substrate — concrete language/library/framework primitives per ecosystem | [pit-of-success-primitives.md](references/pit-of-success-primitives.md) |
| OWASP LLM Top 10 2025 + NIST + ATLAS + Anthropic, with threat → mitigation → review-move | [agent-security.md](references/agent-security.md) |
| Every defense that commonly fails, with source quotes | [false-confidence-traps.md](references/false-confidence-traps.md) |
| STRIDE, LINDDUN, and agent-specific (trifecta-first) threat modeling | [threat-modeling.md](references/threat-modeling.md) |
| Attack classes that SBD + pit-of-success does NOT cover (supply-chain, timing, insider, etc.) | [attack-classes-sbd-misses.md](references/attack-classes-sbd-misses.md) |

## Examples

| Example | Shows |
|---|---|
| [trifecta-triage.md](examples/trifecta-triage.md) | Walking through a real research-assistant agent config: three legs present → cut outbound, isolate content in dual-LLM, narrow data access. End-to-end redesign. |

## Composition with other skills

- **`ci-scaffolds/skills/whitehat`** — the review *posture* half. Finding format (claim + evidence + test + fix + principle + residual), teaching-oriented framing, register-switching (terse vs mastery), escalation to the `mudge` agent.
- **`ci-scaffolds/agents/mudge`** — the review *agent*. Spawn when stakes are high, when compliance claims need testing, when findings need to go in writing with cited evidence and falsifying tests.
- **`guild-arch`** agents — other architectural perspectives (`vector` for attack surface, `burner` for boundaries, `dijkstra` for correctness, `lamport` for distributed reality). Security review often benefits from a focused guild deliberation.
