---
name: whitehat
description: "This skill should be used when the user asks for 'security review', 'write a security finding', 'audit this', 'is this safe to ship', 'teach me about this vulnerability', 'explain this security issue', 'help me understand this attack', 'mudge style review', 'bring in mudge', or when producing a security finding that needs to actually land — actionable, teaching-oriented, with a falsifying test. The review-posture half of security work; composes with trust-boundaries (in guild-arch) for the architectural reasoning."
---

# Whitehat — Review Posture, Teaching, Delivery

Finding a vulnerability is half the job. **Delivering the finding so the developer ends up more capable than when it landed is the other half.** A finding that closes the bug but leaves the developer unchanged has failed: the same class of bug reopens on their next similar task.

This skill is the review-posture half of security work. Its job is how findings get written, when to teach, when to be terse, when to escalate, and how to compose with the reasoning skill that supplies the *what* of the finding.

**This skill composes — it does not replace.** The *architectural reasoning* — trust boundaries, lethal trifecta, SBD principles split into forcing vs posture, pit-of-success primitives, false-confidence traps, attack classes SBD misses, threat modeling, Semgrep/Gitleaks/zizmor scanning — lives in `guild-arch/skills/trust-boundaries`. When doing a security review, load both: trust-boundaries tells you what to look for; whitehat tells you how to deliver what you found. They do not overlap; they stack.

Neither skill claims to be the only security authority. Code-review (correctness), crafting (engineering quality), problem-solving (debugging), architecture (multi-perspective design review), craft-plugins (plugin quality) all have their own scope. Security review sits alongside, not above.

## Contents

- [The posture](#the-posture)
- [The finding template — claim + evidence + test + fix](#the-finding-template)
- [Teaching, not gotcha](#teaching-not-gotcha)
- [The Mudge register — when to be terse](#the-mudge-register)
- [When to escalate to the mudge agent](#when-to-escalate)
- [References](#references)
- [Examples](#examples)

## The posture

The developer is not the adversary. The reviewer and the developer are *on the same side of the table* against the attacker on the other side. This sounds like a platitude; it changes everything about how findings are written.

Four rules:

1. **Specific flaw, specific claim, specific owner.** Name the file, the line, the mechanism, the blast radius, the fix. Vague findings get ignored.
2. **Every finding carries its falsifying test.** "This code is vulnerable" is an assertion. "Run this input, observe this outcome, and the claim fails" is science. See the template below.
3. **Name the class, not just the instance.** The finding's teaching value is in naming the pattern that will generalize to the next handler, the next agent, the next week's code.
4. **Invite the counter.** End with: *"If I'm missing context — tell me."* The reviewer's model of the system is incomplete. The dialogue improves both models.

## The finding template

Every finding carries this shape. It's heavier than a drive-by comment. That's deliberate — the template is the filter. If a finding can't be stated in this form, it isn't ready.

```markdown
## F-NN: <imperative, specific name — what's wrong, not what might be>

**File:** `path/to/file.py:LINE`

**Evidence:** (the exact code, not a description)
```language
<code with context>
```

**Claim:** <one sentence stating the flaw>

**Mechanism:** <the attack chain, narrated. Concrete verbs, concrete inputs.>

**Falsifying test:** <the concrete input/action that would disprove the claim>

**Expected pre-fix:** <attacker benefit observed when test runs>

**Expected post-fix:** <attack denied when test runs>

**Blast radius:** <what the attacker gets when the attack succeeds>

**Fix:** <the concrete code or structural change, pastable>

**Why this fix:** <the [FORCING] principle it honors — from trust-boundaries>

**Residual:** <what the fix does not cover; accepted or separate finding>
```

The full finding style + a worked XSS example + anti-patterns: [examples/review-template.md](examples/review-template.md).

## Teaching, not gotcha

A finding that patches the bug and leaves the developer unchanged has failed. Four moves that turn a finding into an education:

1. **Name the class.** "This is a SQL injection" is shallow. "This is an instance of the injection class — untrusted data reaching an interpreter that treats it as code. Same class as XSS, shell injection, and prompt injection. Fix at the instance: parameterized query. Fix at the class: adopt a typed query builder that makes concatenation impossible." The class generalizes.
2. **Show the attacker's thinking.** First-person narration of the attack chain — reconnaissance, hypothesis, payload, observation, next move. The developer builds an internal adversary this way. Principle without a scene doesn't stick.
3. **Connect the fix to the principle.** "Parameterized queries" is a rule. "Parameterized queries enforce **complete mediation** — the DB driver separates the data path from the code path, so user input cannot cross into interpretation." The principle is the thing the developer carries to the next task.
4. **Invite the counter.** *"If there's context I'm missing — a compensating control upstream, a planned refactor, a reason the pattern looks bad but is actually safe — tell me."* Sometimes the developer knows something you don't. The review is a conversation.

Deeper patterns (dialogue form, "why does this keep happening," class-elimination ladder, patterns that *don't* teach): [references/teaching-security.md](references/teaching-security.md).

## The Mudge register

Mastery orientation is the default posture. It is **not** the only one. Switch to the terse register when:

- The stakes are urgent (production-bound change touching auth/secrets/destructive actions)
- The claim being made in the code or the PR description is demonstrably false
- The pattern being reviewed is a repeat of a finding the team has already been taught and ignored
- The compliance-posture response lands ("we have SOC 2, we have a WAF, we have a SIEM") and the code contradicts the posture

The Mudge register is:

> **F-01: Authentication bypass via client-trusted header.**
> **File:** `auth.py:23` — trusts `X-User-Id` from the request without verification.
> **Claim:** any client sets the header; the handler reads it as authoritative.
> **Falsifying test:** `curl -H "X-User-Id: 1" /api/admin/users` returns admin data.
> **Blast radius:** full authentication bypass.
> **Fix:** remove client-header auth; authenticate via session token validated server-side.
> **Why this fix:** complete mediation + fail-safe defaults — the server does not trust the client to name itself.
> **Pattern:** third handler this quarter that trusts a client-controlled auth header. Add a middleware that strips client-set auth headers at the edge; make the class impossible to reintroduce.

Terse. Specific. No rhetorical wrapper. The final sentence names the pattern at the architectural level. Terseness is respect — the reviewer trusts the developer to handle the finding without a cushion. Reserve it for when teaching has already been offered and the signal now is about *urgency* or *pattern-persistence*.

## When to escalate

Stay in-skill for: design-time review, principle checks, ad-hoc PR review, routine reviews where teaching is the main value.

**Invoke the `mudge` agent for:**

- System-wide security posture review
- Reviewing an agent configuration that approaches the lethal trifecta
- Production-bound changes touching auth, secrets, cross-boundary outbound
- Reviewing compliance-posture claims against what the code actually does
- Writing the final finding report that goes in writing with cited evidence and falsifying tests
- Any time someone says "don't worry, we have a WAF / SOC 2 / guardrail / ML filter"

The mudge agent is an output-shape discipline, not a costume. It produces findings in the register above — specific, falsifiable, cited, pattern-named — and refuses "it depends" framings when the evidence is in the code.

## References

| Need | Reference |
|---|---|
| Finding template, field-by-field with worked XSS example, anti-patterns | [review-template.md](examples/review-template.md) |
| Teaching patterns — dialogue form, class elimination ladder, when to teach vs terse | [teaching-security.md](references/teaching-security.md) |

## For the reasoning half

Load `guild-arch/skills/trust-boundaries` for:

- SBD principles tagged [FORCING] vs [POSTURE] with structural mechanisms
- Lethal trifecta frame + Rule of Two + trifecta triage walkthrough
- Pit-of-success primitives — language/library/framework substrate per ecosystem
- OWASP LLM Top 10 + NIST AI 100-2 + ATLAS threat catalog
- False-confidence traps — every defense that commonly fails
- STRIDE, LINDDUN, agent-specific threat modeling
- Attack classes SBD misses (supply-chain, timing, insider, etc.)
- Semgrep bundled rules (injection, secrets, agent-security, cicd)
- Scanner wrapper with Semgrep + Gitleaks + optional zizmor for GitHub Actions
