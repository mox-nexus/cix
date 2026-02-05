# Prompt Engineering: Methodology

Why these patterns exist and the research behind them.

---

## The Core Problem

Different model architectures need different prompting techniques. What works for autoregressive models (Claude, GPT-4) fails for reasoning models (o1, Deep Think), and vice versa.

| Model Type | How It Works | Prompting Approach |
|------------|--------------|-------------------|
| Autoregressive | Token-by-token generation | Guide the path (CoT, examples) |
| Reasoning/RL | Internal search with verification | Constrain the search space |

---

## Why Architecture Matters

### Autoregressive Models (Claude, GPT-4)

These models generate sequentially. Each token depends on previous tokens. They benefit from:
- Chain-of-thought (shows the path)
- Examples (demonstrates patterns)
- Structured output (guides format)

The prompt **leads** the generation.

### Reasoning Models (o1, Deep Think)

These models have internal reinforcement learning. They explore solution spaces and verify internally. They need:
- Destination definition (not path)
- Hard constraints (electric fences)
- Negative constraints (remove easy outs)

The prompt **bounds** the search.

**Key insight:** Telling o1 "think step by step" is redundant—it already does. You're wasting tokens on instructions the model doesn't need.

---

## Evidence Hierarchy

All technique recommendations follow this hierarchy:

| Level | Source Type | Example |
|-------|-------------|---------|
| **Strong** | Peer-reviewed, replicated | Many-shot ICL paper (ACL/NeurIPS 2024) |
| **Moderate** | Single quality study, converging evidence | Prompt repetition (Google, Dec 2025) |
| **Weak** | Practitioner consensus, theoretical | Style analysis patterns |
| **Speculative** | Reasonable inference | Combined technique effects |

When evidence is limited, we say so.

---

## Key Research Findings

### Many-Shot ICL (2024)

**Finding:** Performance consistently improves with more examples, often peaking at 50-100 shots rather than the traditional 3-5.

**Implication:** "Few-shot" is a misnomer. More examples = better, up to context limits.

**Source:** [Many-Shot In-Context Learning](https://arxiv.org/abs/2404.11018) — ACL/NeurIPS 2024

### Prompt Repetition (Dec 2025)

**Finding:** Simply repeating the prompt (`<QUERY><QUERY>`) improves accuracy. 47 wins out of 70 benchmark-model tests, 0 losses.

**Why it works:** Causal models process sequentially—earlier tokens can't attend to later ones. Repetition allows full cross-attention.

**Source:** [Prompt Repetition Improves Non-Reasoning LLMs](https://arxiv.org/abs/2512.14982) — Google Research

### Chain-of-Verification (CoVe)

**Finding:** Independent verification of claims reduces hallucination by 50-70%.

**Why it works:** Decoupling verification from generation prevents confirmation bias.

**Source:** Meta Research, ACL 2024

### Style Transfer Limits

**Finding:** LLMs have persistent "fingerprints"—noun-heavy, formal, underuse of discourse markers—that prompting can shift but not eliminate entirely.

**Implication:** ~80% style match ceiling with prompting alone. Fine-tuning needed for higher fidelity.

**Source:** Multiple papers on LLM stylistic fingerprints (2024-2025)

---

## Design Principles

### 1. Technique Selection by Architecture

Don't apply autoregressive techniques to reasoning models or vice versa.

| Technique | Autoregressive | Reasoning |
|-----------|---------------|-----------|
| Chain-of-thought | Helps | Redundant |
| Few-shot examples | Helps | Can hurt |
| Detailed prompts | Helps | Can hurt |
| Hard constraints | Optional | Essential |

### 2. Evidence Over Intuition

Every technique claim should have:
- The claim (what it does)
- The effect size (how much)
- The evidence level (how confident)
- The source (where from)

### 3. Show Uncertainty

When evidence is limited:
```
✅ "This is speculative—no direct research, but analogous findings suggest..."
❌ "Research shows..." (when it doesn't)
```

### 4. Composability

Skills are orthogonal. Each covers one domain:
- `deep-reasoning` — Reasoning model constraints
- `deep-research` — Hallucination reduction, verification
- `synthesize-papers` — Multi-paper analysis
- `assimilate-writing` — Style replication

Combine as needed for complex tasks.

---

## The Verification Imperative

Claims made without verification propagate errors. Every skill includes verification patterns:

- **deep-research**: Chain-of-Verification (CoVe) for factual claims
- **synthesize-papers**: Dual-LLM cross-critique for extraction
- **assimilate-writing**: Log-probability scoring for style match

Verification isn't optional—it's how you know the technique worked.

---

See [sources.md](sources.md) for full bibliography.
