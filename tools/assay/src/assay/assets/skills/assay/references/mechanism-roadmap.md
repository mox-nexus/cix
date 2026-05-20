# Mechanism Roadmap

Phase 1 ships ONE mechanism: `cross_family`. The Mechanism port is the seam that admits four additional mechanism families without domain change. Each Phase-3 mechanism tests a different failure mode — they are complementary, not redundant.

## Why multiple mechanisms

Single-mechanism verification is one-trick. The class of errors a verifier catches is bounded by what the mechanism measures.

| Mechanism | Failure mode it catches | Failure mode it misses |
|---|---|---|
| cross_family | Per-voice reading errors, per-family training-set bias | "All three voices got the same wrong answer because they all paraphrased from the same training memory of this 10-K" |
| trace_budget | "Voice paraphrased from training, not from the cited span" | Voice answers correctly but with low confidence |
| semantic_entropy | Voice's own uncertainty about its answer | Confident wrong answers |
| debate | Answer doesn't survive adversarial pressure | Mechanisms that share a training-set blind spot |
| linguistic | Verb-substitution, hedge drift, citation-span misalignment | Conceptual errors that share the same vocabulary |

A mature verification harness composes ALL of them. Each catches what the others miss.

## Phase 3 — trace_budget

**Source**: [leochlon/hallbayes](https://github.com/leochlon/hallbayes) (1,660 ⭐); also implemented as `larsboes/anti-hallucination-mcp`.

**Mechanism**: measure KL divergence between p(claim | full context) and p(claim | context with cited span scrubbed). Low divergence ⇒ the model wasn't actually using the cited span ⇒ it's paraphrasing from training memory ⇒ flag.

**What it adds**: directly tests whether the cite-then-claim relationship is real. This is the single most forensically interesting hallucination test — it asks "did the cited evidence actually condition this answer."

**Backend requirement**: must expose token logprobs. Anthropic API does NOT expose logprobs (confirmed in their docs); Gemini and local MLX do. The trace_budget mechanism wraps a logprob-exposing voice.

**Integration sketch**:

```
adapters/_out/mechanisms/trace_budget/
├── mechanism.py          # implements Mechanism port
├── config.py             # which voice backend; KL threshold; scrub strategy
└── voice_logprob/        # internal sub-port for logprob-exposing voices
    ├── port.py
    ├── gemini.py
    └── mlx_server.py
```

The MechanismResult emits `verdict: AGREE | DISAGREE` plus `evidence: {kl_divergence: float, scrubbed_prompt_sha: str}`.

## Phase 3 — semantic_entropy

**Source**: Farquhar et al., [Nature 2024](https://www.nature.com/articles/s41586-024-07421-0); Kossen et al., [arXiv:2406.15927](https://arxiv.org/abs/2406.15927) (SEPs — single-pass approximation).

**Mechanism**: Train a linear probe on the model's hidden states to estimate semantic entropy from a single generation. High entropy ⇒ model uncertain about the answer ⇒ low-confidence verdict.

**What it adds**: per-claim continuous uncertainty score, not just discrete verdict. Useful as a calibration signal feeding G6 CoVE tier and Adjudication's hold-by-default rule.

**Backend requirement**: must expose hidden states. Local MLX only — closed APIs don't expose hidden states.

**Integration sketch**:

```
adapters/_out/mechanisms/semantic_entropy/
├── mechanism.py
├── config.py             # probe path; uncertainty threshold; sample count if multi-pass
├── probe.py              # the trained linear probe
└── mlx_hidden_state.py   # adapter for extracting hidden states from MLX inference
```

MechanismResult emits `verdict: AGREE | UNCERTAIN` (treats UNCERTAIN as soft-DISAGREE) plus `evidence: {entropy: float, probe_version: str}`.

## Phase 3 — debate

**Source**: Du et al., ICML 2024 ([arXiv:2305.14325](https://arxiv.org/pdf/2305.14325)).

**Mechanism**: voices iteratively respond to each other's critiques across N rounds. Distinct from `cross_family` (which is parallel single-shot critique) — debate is sequential, multi-turn, adversarial.

**What it adds**: addresses the cross_family weak spot of correlated training memory. If three voices all converge on a wrong answer because they share a training-set bias, debate forces them to defend their reasoning against each other; the bias doesn't survive critique as cleanly as the answer does.

**Backend requirement**: multi-turn-capable backends (all of anthropic, gemini-cli, mlx-server are multi-turn-capable).

**Integration sketch**:

```
adapters/_out/mechanisms/debate/
├── mechanism.py
├── config.py             # voices; rounds (default 2); convergence-or-split rule
├── orchestrator.py       # multi-turn coordinator
└── transcript.py         # debate transcript persistence
```

MechanismResult emits `verdict: AGREE | DISAGREE | UNCERTAIN` plus `evidence: {transcript: list[turn], converged_round: int | null}`.

## Phase 3 — linguistic

**Source**: UDPipe ([Universal Dependencies](https://universaldependencies.org/)) via the cix `vaani` package.

**Mechanism**: deterministic NLP checks (no LLM in the loop):
- **Verb fidelity**: extract verbs from source and from voice's reading; flag substitution. Catches "elected to award" → "exercised discretion to approve" drift.
- **Hedge detection**: POS-aware detection of hedge words ("approximately", "roughly", modal verbs) in voice readings.
- **Numeric normalization**: token-aware comparison of "$99M" / "$99 million" / "99000000".
- **Citation-span alignment**: verify the voice's claimed verbatim phrase actually appears in the source.

**What it adds**: catches a class of errors no LLM-internal mechanism reliably catches — subtle verb substitutions, hedge drift, numeric-format aliasing. Pure deterministic; no model dependency.

**Backend requirement**: vaani Rust core + UDPipe English model (~16 MB on first run).

**Integration sketch**:

```
adapters/_out/mechanisms/linguistic/
├── mechanism.py
├── config.py             # which checks to run; hedge/verb dictionaries
├── verb_fidelity.py
├── hedge_detection.py
├── numeric_normalize.py
└── citation_align.py
```

Each check produces a sub-result; the mechanism aggregates to `verdict: AGREE | DISAGREE` plus `evidence: {checks: dict[name, result]}`.

## Composing mechanisms

The Adjudication service in domain operates over the Verdict alone, not over mechanism-specific evidence. When all five mechanisms run, the Adjudication reasons over five Verdicts:

```
adjudicate(claim_id, [
    MechanismResult(mechanism="cross_family",     verdict=AGREE,    evidence={...}),
    MechanismResult(mechanism="trace_budget",     verdict=DISAGREE, evidence={"kl_divergence": 0.03, ...}),
    MechanismResult(mechanism="semantic_entropy", verdict=AGREE,    evidence={"entropy": 0.4, ...}),
    MechanismResult(mechanism="debate",           verdict=AGREE,    evidence={...}),
    MechanismResult(mechanism="linguistic",       verdict=AGREE,    evidence={"checks": {...}}),
])
→ Adjudication(diverged=True, final_verdict=UNCERTAIN, ...)
```

Divergence triggers human review. The reviewer reads the diverging mechanism's evidence dict to understand WHY it disagreed — trace_budget's KL number, the linguistic check's verb substitution, etc.

## Implementation order (suggested)

1. **trace_budget first** — most forensically distinctive (cite-actually-conditioned-the-answer test); ~3 days engineering on Gemini backend.
2. **linguistic** — pure deterministic, no LLM dependency, fast to implement; ~2 days on top of vaani.
3. **semantic_entropy** — requires MLX-only path and a trained probe; ~5 days.
4. **debate** — most complex orchestration; defer to after the others are validated.

## What stays the same

The Mechanism port and the MechanismResult contract do not change for any of the above. The InquiryRunner keeps iterating `for claim in store: for mechanism in mechanisms: mechanism.evaluate(claim)` regardless of which mechanism families are wired. Adjudication keeps reasoning over Verdicts.

The cobble Phase 1 architecture is what makes Phase 3 a series of additions, not a rewrite.
