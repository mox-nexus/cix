---
name: auditing
description: "This skill should be used when the user asks to 'audit the research', 'check provenance', 'trace claims to sources', 'verify the chain', or needs end-to-end quality assurance on research outputs."
version: 0.1.0
---

# Auditing

> The audit traces a claim from finding back to source quote. If the chain breaks, the finding falls.

Auditing is the quality gate for research. It traces the provenance chain end-to-end: from synthesis findings, through verified claims, back to extracted quotes, back to source text. Every link must hold. A finding with a broken chain is an ungrounded assertion, regardless of how plausible it sounds.

## Contents

- [The Provenance Chain](#the-provenance-chain)
- [Audit Protocol](#audit-protocol)
- [Chain Integrity Checks](#chain-integrity-checks)
- [Confidence Calibration](#confidence-calibration)
- [The Verdict](#the-verdict)
- [Output Format](#output-format)
- [Anti-Patterns](#anti-patterns)

## The Provenance Chain

Every research finding has a chain:

```
Source text (original paper)
  → Source quote (verbatim, with location)       [extraction]
  → Extracted claim [source:cN]                  [extraction]
  → Verification verdict                         [verification]
  → Synthesized finding with claim references     [synthesis]
```

The audit walks this chain in reverse — starting from findings, tracing back to sources.

### What Can Break

| Break Point | Symptom | Consequence |
|-------------|---------|-------------|
| Quote doesn't exist in source | Fabricated evidence | Finding ungrounded |
| Claim doesn't follow from quote | Interpretation error | Finding distorted |
| Verification was rubber-stamped | False confidence | Error propagated |
| Finding cites unverified claim | Provenance gap | Chain incomplete |
| Finding overstates claim scope | Scope inflation | Misleading conclusion |

## Audit Protocol

### Phase 1: Chain Completeness

For each finding in the synthesis:
1. **List all claim references** ([source:cN]) cited as evidence
2. **Check each claim has a verification record** — VERIFIED or CORRECTED
3. **Check each claim has an extraction record** — QUOTE + LOCATION + CLAIM
4. **Flag any finding that references claims without complete chains**

### Phase 2: Chain Accuracy (Sampling)

Full verification of every chain is expensive. Sample strategically:

| Finding Type | Sampling Rate | Rationale |
|-------------|---------------|-----------|
| HIGH confidence findings | 100% — verify every chain | These are your strongest claims |
| MEDIUM confidence findings | 50% — random sample | Spot-check for systematic errors |
| LOW confidence findings | 25% — random sample | Already flagged as weak |
| Key numbers (cited in summary) | 100% | Numbers travel — errors compound |

For each sampled chain:
1. **Read the source** at the claimed location
2. **Confirm the quote is verbatim**
3. **Confirm the claim follows from the quote**
4. **Confirm the finding follows from the verified claims**
5. **Confirm the confidence level is warranted by the evidence pattern**

### Phase 3: Scope Check

For each finding:
- Does the finding claim more than the evidence supports?
- Are boundary conditions from sources preserved in the finding?
- Is the population scope correct? (not overgeneralized)
- Is the causal language appropriate for the study designs cited?

### Phase 4: Completeness Check

Review against scope.md:
- Are all research questions addressed?
- Are gaps explicitly named (not silently skipped)?
- Are negative results reported?
- Are conflicting findings preserved (not silently resolved)?

## Chain Integrity Checks

### The Number Check

Every number in a finding must trace to a specific source:

```
Finding says: β=0.507
  → Synthesis references: [blaurock2025:c1]
  → Verification: VERIFIED (β=0.507 confirmed)
  → Extraction quote: "user control had the strongest effect... (β=0.507, p<0.001)"
  → Source page: Results section, paragraph 3
  ✓ Chain intact
```

If any link differs:

```
Finding says: β=0.51
  → Synthesis references: [blaurock2025:c1]
  → Extraction says: β=0.507
  ✗ ROUNDING ERROR — finding rounds without noting approximation
```

### The Scope Check

Every generalization must be warranted:

```
Finding says: "Control improves outcomes"
  → Evidence: 3 studies, all with US university samples
  ✗ SCOPE INFLATION — finding should say "Control improves outcomes
    in US university settings" or note the population limitation
```

### The Causation Check

Causal language must match study design:

```
Finding says: "Transparency causes trust"
  → Evidence: [study:c3] — cross-sectional survey
  ✗ CAUSAL OVERREACH — survey design supports "is associated with,"
    not "causes"
```

### The Confidence Check

Confidence levels must match evidence patterns:

```
Finding says: CONFIDENCE: HIGH
  → Evidence: single study, n=89, quasi-experimental
  ✗ CONFIDENCE INFLATION — single study without replication is
    MEDIUM at best, LOW given small sample
```

## Confidence Calibration

The audit calibrates confidence across all findings:

| Check | Expected |
|-------|----------|
| HIGH findings have 3+ converging sources including Tier 1? | Yes |
| MEDIUM findings have 2+ sources or single Tier 1? | Yes |
| No LOW findings upgraded without new evidence? | Yes |
| No INSUFFICIENT gaps presented as findings? | Yes |
| Confidence never increased through pipeline? | Yes |

If calibration fails, flag the specific findings for downgrade.

## The Verdict

**SHIP** or **RETURN**. No middle ground.

### SHIP Criteria

All must pass:
- [ ] Every HIGH confidence finding has a complete, verified chain
- [ ] Sampled chains for MEDIUM/LOW findings check out
- [ ] No scope inflation in findings
- [ ] No causal overreach
- [ ] Confidence levels calibrated
- [ ] All research questions addressed (or gaps explicitly named)
- [ ] Negative results included
- [ ] Divergences preserved (not silently resolved)

### RETURN Criteria

Any single failure → RETURN with specific remediation:

| Failure | Return To | Remediation |
|---------|-----------|-------------|
| Broken chain (quote not found) | extract | Re-extract from source |
| Claim doesn't follow from quote | extract | Re-extract with correct interpretation |
| Verification rubber-stamped | scrutiny | Full CoVE on flagged claims |
| Finding cites unverified claim | scrutiny | Verify the missing claims |
| Scope inflation | synthesis | Narrow finding scope to evidence |
| Causal overreach | synthesis | Adjust causal language |
| Confidence inflation | synthesis | Recalibrate confidence levels |
| Research question unanswered | synthesis | Address or name gap |
| Missing negative results | synthesis | Include null findings |

## Output Format

```markdown
# Audit Report

## Scope
- Research questions audited: [list from scope.md]
- Findings audited: [N]
- Chains sampled: [N] / [total]

## Chain Integrity

### Complete Chains
- [finding]: [source:cN] → extraction → verification → synthesis ✓
- ...

### Broken Chains
- [finding]: [source:cN] — [break point] — [what's wrong]
- ...

## Scope Check
- [Any scope inflation found]

## Causation Check
- [Any causal overreach found]

## Confidence Calibration
- [Any confidence mismatches]

## Completeness
- Research questions addressed: [list]
- Research questions with gaps: [list]
- Negative results: [included/missing]
- Divergences: [preserved/silently resolved]

## Verdict: [SHIP / RETURN]

### If RETURN:
| Issue | Return To | Remediation |
|-------|-----------|-------------|
| [specific issue] | [agent] | [specific fix] |
```

## Anti-Patterns

| Anti-Pattern | Why It Fails | Do Instead |
|--------------|-------------|------------|
| **Trusting the pipeline** | Each stage can introduce errors | Verify end-to-end independently |
| **Spot-checking only easy claims** | Biased sample misses systematic errors | Random sampling + 100% of HIGH claims |
| **Accepting plausible chains** | "Sounds right" is not verification | Walk the actual chain in the files |
| **Auditing without sources** | Can't verify quotes without originals | Have source material available |
| **Rubber-stamping SHIP** | Defeats the quality gate | Every SHIP requires evidence |
| **Rewriting instead of returning** | Audit evaluates, doesn't transform | Return to the appropriate agent |

## References

- `references/provenance-chain.md` — Chain structure, integrity checks, worked audit example
