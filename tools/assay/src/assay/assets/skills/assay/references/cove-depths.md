# CoVE Depths — ANCHORED / REEXTRACT / BLIND

The `cross_family` mechanism dispatches voices to one of three Chain-of-Verification depths per Dhuliawala et al. 2023 ([arXiv:2309.11495](https://arxiv.org/abs/2309.11495)). Each names what the voice is allowed to see when answering. Independence from the candidate claim is the mechanism; depth controls how much that independence is preserved.

## ANCHORED

The voice receives the claim AND the source. The ask is "does the source support the claim as written."

**Catches**: transcription errors only. The voice sees both halves, can confirm they match.

**Misses**: framing errors (the claim is phrased to anchor the verifier toward agreement), selection-bias errors (the claim picked the wrong cell), and convention errors (the claim used a non-standard convention; the verifier confirms under the same wrong convention).

**Use when**: spot-checking large numeric fact tables where transcription is the dominant failure mode.

**Example prompt** (rendered by `prompt_builder.py`):

> CLAIM: EXPE FY2025 SBC capitalization rate is 19.9%
> SOURCE EXCERPT: ... We capitalized $99 million of stock-based compensation expense ... total stock-based compensation expense of $497 million ...
> Does the source excerpt support the claim as written?

The voice can compute 99/497 ≈ 19.9% and confirm. Clean.

## REEXTRACT

The voice receives the source and the question. It re-derives the value independently. The application layer compares the voice's `EXTRACTED:` field to the claim's `expected_value`.

**Catches**: transcription + selection-bias. The voice picks the cell on its own; if the original claim picked the wrong cell, the voice's pick disagrees and the divergence surfaces.

**Misses**: convention errors (if the question is phrased to assume the same convention as the claim), framing errors at the question level.

**Use when**: this is the default. Most value-bearing claims belong here.

**Example prompt**:

> QUESTION: What is the SBC capitalization rate for FY2025?
> ASSERTED VALUE: 19.9%
> SOURCE EXCERPT: ...
> [voice extracts independently, compares to 19.9%]

## BLIND

The voice sees ONLY the source and a neutrally-phrased question. No claim. No expected value. No anchoring framing. The voice answers cold; comparison happens in the application layer.

**Catches**: transcription + selection + framing errors. The voice cannot be biased toward confirming what it doesn't see.

This is the form Dhuliawala 2023 calls true CoVE: the verifier is independent of the candidate answer.

**Cost**: longer prompts (~5–15KB excerpt typical), longer voice latency, free-form output that's harder to mechanically compare. Reserve for claims where framing matters most.

**Use when**:
- Executive-summary statements ("EXPE FY2025 outperformed peers by 44.7pp" — reframing risk)
- "Things to note" sentences ("the cap rate stepped up +4.9pp FY2024→FY2025, the largest in the series" — selection-of-emphasis risk)
- Verb-fidelity-sensitive claims ("the Committee exercised discretion to approve" vs the filing's actual verb)
- Convention-sensitive claims ("cap rate = 19.9%" — depending on Cap/Expensed vs Cap/(Expensed+Cap) convention)

**Example prompt**:

> QUESTION: What does the source disclose about SBC capitalization for FY2025?
> SOURCE EXCERPT: ...
> [voice answers cold, picks its own convention, picks its own emphasis]
> EXTRACTED: ...
> SUPPORTING SPAN: ...

If the voice independently picks Cap/(Expensed+Cap) = 99/(99+398) = 19.9%, the convention agrees. If it picks Cap/Expensed = 99/398 = 24.9%, the divergence surfaces — that's the diagnostic.

## Worked example: the L2 trap

The case-eg-research campaign hit this in finding F003: the original cap rate convention was Cap/Expensed (24.9% FY2025), not the forensic convention Cap/(Expensed+Cap) (19.9%). Under ANCHORED or REEXTRACT depth (with the question pre-framed to use the same convention), all three voices would have confirmed 24.9%. Under BLIND depth, the voices independently pick the convention they think is right, and the convention-disagreement surfaces.

This is why BLIND is reserved for high-stakes claims: it's the only depth that catches convention-bias errors a single-family panel will all share.

## Mission YAML

Set the default depth at the mechanism config level:

```yaml
mechanisms:
  - name: cross_family
    config:
      depth: blind   # one of: anchored | reextract | blind
      voices:
        ...
```

Per-claim depth override is not yet supported — planned. Workaround: split high-stakes claims into a separate inquiry with `depth: blind` and run the bulk inquiry with `depth: reextract`.

## When to escalate to BLIND

Escalate if any of these are true for the claim:
- The claim's stated value depends on a convention that has more than one valid form
- The claim is rolled-up across multiple primary cells (synthesis-style claim)
- The claim uses verbs that the source might use differently
- The claim emphasizes one of several plausible patterns in the same data
- A defense reader could plausibly say "you framed the question to get that answer"
