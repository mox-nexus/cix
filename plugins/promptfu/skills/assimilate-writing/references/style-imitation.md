# Style Imitation Prompting

Engineering prompts to replicate writing style and voice from examples.

> **Sources:** Research from 2024-2026, Google Research, arXiv papers

---

## The Problem

LLMs have distinctive "fingerprints" that persist across prompting attempts:
- Noun-heavy, informationally dense defaults
- Underuse of hedges ("perhaps", "maybe") and boosters ("clearly", "obviously")
- Formal tone bias from instruction tuning

Style imitation requires overriding these defaults with target patterns.

---

## Evidence-Backed Techniques

### What Works

| Technique | Effect Size | Source |
|-----------|-------------|--------|
| **Many-shot (50-100 examples)** | 23-50% improvement | Many-Shot ICL (ACL/NeurIPS 2024) |
| **Analyze-first pattern** | 30-50% improvement | CoT literature extrapolation |
| **Prompt repetition** | 47/70 wins, 0 losses | Google Research (Dec 2025) |
| **Persona + examples hybrid** | 15-30% improvement | Role prompting + ICL studies |
| **Iterative refinement** | 10-20% improvement | Paraphrasing studies |
| **OSST (neutralize→transfer)** | Outperforms baselines | arXiv:2510.13302 (Oct 2025) |

### What Doesn't Work

| Technique | Finding | Source |
|-----------|---------|--------|
| Zero-shot persona alone | 2-8% improvement only | Meta-analysis |
| 3-5 examples | Insufficient for style | Many-shot ICL paper |
| "Write in X style" without examples | Near-zero effect | Practitioner consensus |
| Mixed-domain examples | Confuses style learning | Style transfer research |

---

## Core Pattern: Analyze Then Apply

The single biggest lever for style imitation.

### Why It Works

LLMs are better at **explicit reasoning** than implicit pattern matching. Forcing style analysis creates an intermediate representation the model can follow.

### Prompt Structure

```markdown
Here are examples of my writing:

---
[Example 1 - 300-500 words]
---
[Example 2 - different topic, same voice]
---
[Example 3 - shows stylistic variations]
---

Before writing anything, analyze my style:

1. **Sentence patterns**: Length, rhythm, complexity
2. **Word choice**: Formal/casual, technical terms, favorite words
3. **Punctuation**: Em-dashes, ellipses, parentheses, commas
4. **Tone**: Confident/hedging, personal/impersonal, dry/warm
5. **Structure**: How I open, transition, close
6. **Quirks**: Anything distinctive

Now write [TASK] matching exactly those characteristics.
```

### Grounding Variant

If analysis is too vague, add evidence requirement:

```markdown
For each characteristic you identify, quote a specific phrase
from the examples that demonstrates it. If you can't find evidence,
revise your analysis.
```

---

## Prompt Repetition (December 2025)

Dead simple technique from Google Research.

### The Technique

Transform `<QUERY>` → `<QUERY><QUERY>`

Just repeat the entire prompt twice.

### Why It Works

Causal LLMs process tokens sequentially — earlier tokens can't attend to later ones. Repetition allows all tokens in the second copy to attend to all tokens in the first.

### Results

- 47 wins out of 70 benchmark-model tests
- 0 losses
- One task: 21% → 97% accuracy
- No output length increase
- No latency penalty (prefill stage)

### When to Use

| Scenario | Effect |
|----------|--------|
| Non-reasoning tasks | Strong improvement |
| Reasoning enabled (CoT) | Neutral (already internally repeats) |
| Style imitation | Likely helpful (untested directly) |

### Application to Style

```markdown
[BEGIN STYLE PROMPT]
Here are examples of my writing:
[examples]
Analyze my style, then write [task] in my voice.
[END STYLE PROMPT]

[BEGIN STYLE PROMPT]
Here are examples of my writing:
[examples]
Analyze my style, then write [task] in my voice.
[END STYLE PROMPT]
```

**Source:** [Prompt Repetition Improves Non-Reasoning LLMs](https://arxiv.org/abs/2512.14982) (Leviathan et al., Google Research, Dec 2025)

---

## OSST: One-Shot Style Transfer

Advanced technique using content neutralization.

### Core Insight

Instead of showing style examples directly, show the **transformation** from neutral to styled.

### The Three Steps

```
1. NEUTRALIZE
   Original text → strip style → neutral version

2. DEMONSTRATE TRANSFORMATION
   Show neutral→styled pair as implicit style definition

3. APPLY TRANSFORMATION
   New neutral content → apply learned transformation
```

### Prompt Pattern

```markdown
Here's a piece of writing and its neutral version:

NEUTRAL VERSION:
[Content stripped of style - just facts]

STYLED VERSION (how I actually wrote it):
[Your original writing]

The transformation from neutral to styled captures my voice.

Now apply the same transformation to this neutral content:
[New content you want styled]
```

### Why This Works

- Separates **content** from **style** explicitly
- Model learns the transformation, not just the output
- One example often sufficient (vs. many-shot for direct imitation)
- Topic-independent (neutralization removes content bias)

### Scoring with Log-Probabilities

The original OSST paper scores style transfer quality by measuring:

> P(original | neutral + style_example)

Higher probability = better style capture.

**Claude doesn't expose logprobs.** For evaluation, use local models (see below).

**Source:** [LLM one-shot style transfer for Authorship](https://arxiv.org/abs/2510.13302) (Oct 2025)

---

## Local Models for Log-Probability Scoring

Claude and most APIs don't expose token log-probabilities. For OSST-style evaluation:

### Options

| Tool | Logprob Access | Setup Complexity |
|------|----------------|------------------|
| **llama.cpp** | Full | Medium |
| **Ollama** | Via API flag | Low |
| **vLLM** | Full | Medium |
| **Hugging Face** | Full | Low-Medium |

### Ollama (Easiest)

```bash
# Install
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull mistral

# API call with logprobs
curl http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt": "[your prompt]",
  "options": {
    "logprobs": true,
    "top_logprobs": 5
  }
}'
```

### Python with Hugging Face

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "mistralai/Mistral-7B-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)

def get_logprob(prompt: str, continuation: str) -> float:
    """Get log-probability of continuation given prompt."""
    full_text = prompt + continuation
    inputs = tokenizer(full_text, return_tensors="pt")
    prompt_len = len(tokenizer(prompt)["input_ids"])

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    # Get logprobs for continuation tokens only
    log_probs = torch.log_softmax(logits, dim=-1)
    continuation_logprob = 0.0

    for i in range(prompt_len, len(inputs["input_ids"][0])):
        token_id = inputs["input_ids"][0][i]
        continuation_logprob += log_probs[0, i-1, token_id].item()

    return continuation_logprob

# OSST scoring
neutral = "The meeting covered three topics."
styled_original = "We hit three things in the meeting—bang, bang, bang."
style_example = "[one example of target style]"

prompt = f"Style example:\n{style_example}\n\nNeutral:\n{neutral}\n\nStyled:"
score = get_logprob(prompt, styled_original)
print(f"Style match score: {score}")  # Higher = better match
```

### llama.cpp (Most Control)

```bash
# Build with logprobs
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && make

# Run with logprobs
./main -m models/mistral-7b.gguf \
  --prompt "[your prompt]" \
  --logprobs 5
```

### Recommended Models for Style Scoring

| Model | Size | Quality | Speed |
|-------|------|---------|-------|
| Mistral 7B | 7B | Good | Fast |
| Qwen 2.5 7B | 7B | Better | Fast |
| Llama 3.2 3B | 3B | Adequate | Very fast |

For style evaluation specifically, smaller models work fine — you're measuring relative probabilities, not generating quality content.

---

## Many-Shot Guidelines

More examples consistently improves style consistency.

### Optimal Counts

| Use Case | Examples | Context Cost |
|----------|----------|--------------|
| Quick test | 3-5 | ~2K tokens |
| Good consistency | 10-20 | ~5-10K tokens |
| Best results | 50-100 | ~25-50K tokens |

### Example Selection Criteria

1. **Topic variety** — same voice, different subjects
2. **Length variety** — short and long pieces
3. **Include quirks** — even "bad" habits are signal
4. **Recency** — style evolves, weight recent writing

### Diminishing Returns

Performance improves consistently up to ~100 examples, then plateaus. Beyond 200, marginal gains are minimal.

**Source:** [Many-Shot In-Context Learning](https://arxiv.org/abs/2404.11018) (ACL/NeurIPS 2024)

---

## Iterative Refinement

LLM signatures fade through successive paraphrasing.

### Pattern

```markdown
Round 1: [Generate initial output]

Round 2: "Rewrite this to match my style more closely.
         Specifically, adjust [sentence length / word choice / tone]."

Round 3: "One more pass. Make the [specific trait] more pronounced."
```

### Evidence

- Characteristic markers fade noticeably after 3-5 rounds
- Diminishing returns beyond 5 iterations
- Best when targeting specific traits per round

**Source:** [The Erosion of LLM Signatures Through Iterative Paraphrasing](https://arxiv.org/abs/2512.05311) (Dec 2024)

---

## Hard Limits

What prompting cannot overcome:

| Limitation | Why | Mitigation |
|------------|-----|------------|
| Noun-heavy defaults | Instruction tuning bias | Explicit "use more verbs" constraint |
| Discourse marker underuse | Training distribution | List specific markers to include |
| Model fingerprint | Architecture | Accept ~80% style match ceiling |
| Very casual/colloquial | Formal training bias | Hardest to replicate |

---

## Complete Style Imitation Prompt

Combining all techniques:

```markdown
[REPEAT THIS ENTIRE BLOCK TWICE FOR +ACCURACY]

# My Writing Style

## Examples (read all before analyzing)

---
EXAMPLE 1:
[Your writing - 300-500 words]

---
EXAMPLE 2 (different topic):
[Your writing - 300-500 words]

---
EXAMPLE 3 (different topic):
[Your writing - 300-500 words]

---

## Style Analysis (complete before writing)

Analyze my writing across these dimensions. For each, quote specific
evidence from the examples:

1. **Sentence patterns**: Length, rhythm, complexity
   Evidence: "[quote]"

2. **Word choice**: Formal/casual, technical terms, favorites
   Evidence: "[quote]"

3. **Punctuation habits**: Em-dashes, ellipses, parentheses
   Evidence: "[quote]"

4. **Tone markers**: Hedging vs asserting, personal vs impersonal
   Evidence: "[quote]"

5. **Structural patterns**: Openings, transitions, closings
   Evidence: "[quote]"

6. **Distinctive quirks**: Anything unique
   Evidence: "[quote]"

## Task

Now write [YOUR TASK] in my exact voice, matching every dimension above.

[END REPEATED BLOCK]
```

---

## Evaluation Checklist

After generation, verify:

- [ ] Sentence length distribution matches examples
- [ ] Key vocabulary/phrases appear naturally
- [ ] Punctuation patterns preserved
- [ ] Tone consistent (hedging/asserting ratio)
- [ ] No "Claude-isms" (overly formal, noun-heavy)
- [ ] Reads like held-out sample of your writing

---

## Sources

### Core Research
- [Many-Shot In-Context Learning](https://arxiv.org/abs/2404.11018) — ACL/NeurIPS 2024
- [Prompt Repetition Improves Non-Reasoning LLMs](https://arxiv.org/abs/2512.14982) — Google Research, Dec 2025
- [LLM One-Shot Style Transfer](https://arxiv.org/abs/2510.13302) — Oct 2025
- [The Erosion of LLM Signatures](https://arxiv.org/abs/2512.05311) — Dec 2024

### Style Analysis
- [Do LLMs Write Like Humans?](https://www.pnas.org/doi/10.1073/pnas.2422455122) — PNAS
- [Detecting Stylistic Fingerprints](https://arxiv.org/abs/2503.01659) — 2025
- [StyleDistance: Content-Independent Style Embeddings](https://arxiv.org/abs/2410.12757) — 2024

### Prompt Engineering
- [Lakera Prompt Engineering Guide 2026](https://www.lakera.ai/blog/prompt-engineering-guide)
- [Chain-of-Thought Prompting](https://www.promptingguide.ai/techniques/cot)
