# Paper Synthesis Patterns

Extended patterns for analyzing and synthesizing academic papers with LLMs.

---

## The Problem

| Finding | Source |
|---------|--------|
| 75% of multi-document summary content can be hallucinated | Synthesis research (2024) |
| LLMs over-sensitive to input ordering | Position bias studies |
| Citation fabrication rates 20%+ | Deakin University |

**Single-pass synthesis is unreliable.** Multi-stage verification required.

---

## Dual-LLM Cross-Critique

The most validated approach for paper extraction.

### Why It Works

Two models extract independently. When they agree, confidence is high. When they disagree, cross-critique resolves.

### The Protocol

```
Stage 1: Independent Extraction
├── Model A extracts claims from paper
└── Model B extracts claims from paper (no visibility to A)

Stage 2: Concordance Check
├── If A and B agree → HIGH CONFIDENCE
└── If A and B disagree → Stage 3

Stage 3: Cross-Critique
├── Show A's extraction to B: "What's wrong with this?"
├── Show B's extraction to A: "What's wrong with this?"
└── 51% of discordant pairs become concordant

Stage 4: Synthesis
└── Use concordant claims only, flag remaining disagreements
```

### Results

- **0.94 accuracy** on concordant extractions
- **51% resolution** of initial disagreements through critique
- Remaining disagreements flagged for human review

### Prompt Pattern

```markdown
# Model A Prompt
Extract all factual claims from this paper. For each claim:
1. State the claim precisely
2. Quote the supporting text
3. Note any caveats or limitations

Paper: [PAPER TEXT]

# Model B Prompt (same, independent)

# Cross-Critique Prompt
Here is an extraction from another model:
[MODEL A EXTRACTION]

Review this extraction against the original paper:
1. Which claims are accurate?
2. Which claims are unsupported or misrepresented?
3. What claims are missing?

Paper: [PAPER TEXT]
```

---

## Plan-Based Synthesis (LitLLMs)

Structured planning before synthesis reduces hallucination.

### Why It Works

Direct generation ("summarize these papers") hallucinates to fill gaps. Plan-first synthesis:
1. Creates explicit structure
2. Maps content to structure
3. Identifies gaps before filling

### The Protocol

```
Stage 1: Plan Generation
├── Analyze papers for themes
├── Create hierarchical outline
└── Map papers to outline sections

Stage 2: Structured Extraction
├── For each outline section:
│   ├── Extract relevant claims from papers
│   ├── Note agreements and conflicts
│   └── Flag gaps (no paper covers this)

Stage 3: Gap-Aware Synthesis
├── Synthesize where evidence exists
├── Mark gaps explicitly: [NO EVIDENCE]
└── Don't fabricate to fill gaps
```

### Prompt Pattern

```markdown
# Stage 1: Planning
Papers to synthesize:
1. [Paper 1 title + abstract]
2. [Paper 2 title + abstract]
3. [Paper 3 title + abstract]

Create a hierarchical outline for synthesizing these papers:
- What are the major themes?
- What sub-topics exist within each theme?
- Which papers cover which topics?

# Stage 2: Extraction
Using this outline:
[OUTLINE]

For section "[SECTION NAME]", extract relevant claims from each paper:
- Paper 1: [claims or "not addressed"]
- Paper 2: [claims or "not addressed"]
- Paper 3: [claims or "not addressed"]

# Stage 3: Synthesis
Synthesize section "[SECTION NAME]" from these extractions:
[EXTRACTIONS]

Rules:
- Only include claims with paper support
- Mark conflicts: "CONFLICTING: Paper 1 claims X, Paper 2 claims Y"
- Mark gaps: "GAP: No papers address [topic]"
```

---

## Claimify Pipeline

99% claim entailment through structured decomposition.

### The Three Stages

```
Original Text
     ↓
┌─────────────────┐
│   SELECTION     │  Filter non-factual content
│                 │  (opinions, hedges, meta-commentary)
└────────┬────────┘
         ↓
┌─────────────────┐
│ DISAMBIGUATION  │  Resolve pronouns, references
│                 │  ("it" → "the algorithm")
└────────┬────────┘
         ↓
┌─────────────────┐
│  DECOMPOSITION  │  Split compound claims
│                 │  One fact per claim
└────────┬────────┘
         ↓
    Atomic Claims
```

### Why Each Stage Matters

**Selection:** Non-factual content ("We believe...", "It seems...") can't be verified. Remove before processing.

**Disambiguation:** Pronouns and references ("this approach", "the method") are ambiguous. Resolve to specific entities.

**Decomposition:** Compound claims ("X is fast and accurate") hide partial truth. Split into verifiable atoms.

### Prompt Pattern

```markdown
# Selection
Text: "[ORIGINAL]"

Extract only factual claims. Remove:
- Opinions ("we believe", "it seems")
- Meta-commentary ("as discussed above")
- Hedged statements ("might", "could potentially")

Output factual statements only.

# Disambiguation
Claims:
[SELECTED CLAIMS]

For each claim, replace:
- Pronouns → specific nouns
- "this/that" → explicit references
- Abbreviations → full terms (first occurrence)

# Decomposition
Claims:
[DISAMBIGUATED CLAIMS]

Split compound claims into atomic facts:
- One verifiable fact per claim
- No conjunctions joining separate facts
- Each claim independently true or false
```

---

## Four-Layer Gap Analysis

Systematic identification of research gaps.

### The Framework

| Layer | Question | Example Gap |
|-------|----------|-------------|
| **Theoretical** | What constructs lack formal definition? | "No formal model of X" |
| **Methodological** | What approaches haven't been tried? | "No longitudinal studies" |
| **Empirical** | What populations/contexts unstudied? | "No data from domain Y" |
| **Practical** | What implementations missing? | "No production deployments" |

### Prompt Pattern

```markdown
Based on these papers:
[PAPER SUMMARIES]

Identify gaps at each layer:

1. THEORETICAL GAPS
   - What concepts are undefined or poorly defined?
   - What theoretical frameworks are missing?

2. METHODOLOGICAL GAPS
   - What research methods haven't been applied?
   - What study designs are missing?

3. EMPIRICAL GAPS
   - What populations haven't been studied?
   - What contexts lack data?

4. PRACTICAL GAPS
   - What implementations are missing?
   - What real-world validations are needed?

For each gap, explain:
- Why it matters
- What addressing it would enable
```

---

## Evidence Weighting

When findings conflict, weight by research quality.

### Hierarchy

```
RCT (randomized controlled trial)
     ↓
Quasi-experimental
     ↓
Longitudinal observational
     ↓
Cross-sectional
     ↓
Case study
     ↓
Expert opinion
```

### Weighting Factors

| Factor | Higher Weight | Lower Weight |
|--------|--------------|--------------|
| Design | RCT, meta-analysis | Case study |
| Sample | n > 1000 | n < 50 |
| Recency | Past 2 years | > 5 years |
| Replication | Replicated | Single study |
| Venue | Top-tier peer-reviewed | Preprint, blog |

### Prompt Pattern

```markdown
These papers have conflicting findings on [TOPIC]:

Paper A: [FINDING] (n=[N], design=[DESIGN], year=[YEAR], venue=[VENUE])
Paper B: [FINDING] (n=[N], design=[DESIGN], year=[YEAR], venue=[VENUE])

Weight the evidence:
1. Which has stronger study design?
2. Which has larger sample?
3. Which is more recent?
4. Are either replicated?

Synthesize: Given this weighting, what's the best current understanding?
```

---

## Position Bias Mitigation

LLMs favor information based on position, not importance.

### The Problem

- Information at start/end weighted more heavily
- Middle content often ignored
- Order of papers affects synthesis

### Mitigations

**1. Multiple orderings:**
```markdown
Run synthesis 3 times with different paper orders:
- Order 1: [A, B, C]
- Order 2: [B, C, A]
- Order 3: [C, A, B]

Only include claims that appear in all 3 syntheses.
```

**2. Per-paper extraction first:**
```markdown
Extract claims from each paper separately.
Then synthesize from claim lists, not papers.
```

**3. Explicit importance:**
```markdown
Before synthesizing, rank papers by:
- Relevance to question (1-5)
- Methodological quality (1-5)
- Recency (1-5)

Use these rankings to weight contributions.
```

---

## Complete Synthesis Workflow

```
Input: Multiple papers on topic

1. PLAN
   └── Create hierarchical outline from abstracts

2. EXTRACT (per paper)
   ├── Claimify: select → disambiguate → decompose
   └── Map claims to outline sections

3. VERIFY (dual-LLM)
   ├── Second model extracts independently
   ├── Cross-critique disagreements
   └── Flag unresolved conflicts

4. SYNTHESIZE (per section)
   ├── Aggregate concordant claims
   ├── Weight conflicting evidence
   └── Mark gaps explicitly

5. GAP ANALYSIS
   └── Four-layer review: theoretical, methodological, empirical, practical

Output: Verified synthesis with explicit gaps and conflicts
```

---

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|---------|--------------|
| Single-pass synthesis | Multi-stage with verification |
| Trust LLM citations | Verify all citations exist |
| Ignore conflicts | Surface and weight them |
| Fill gaps with inference | Mark gaps explicitly |
| Process all papers together | Extract per-paper first |
| Fixed paper order | Multiple orderings or randomize |
