---
name: assimilate-writing
description: "Use when: 'write in my style', 'imitate my writing', 'replicate my voice', 'match my tone', 'style transfer', 'few-shot style', 'write like me', 'capture my voice', or getting LLMs to replicate writing style from examples."
---

# Assimilate Writing

Getting LLMs to replicate writing style and voice from examples.

**The problem:** LLMs have fingerprints — noun-heavy, formal, underuse hedges/boosters — that persist across prompting.

---

## What Works

| Technique | Effect | Source |
|-----------|--------|--------|
| **Analyze-first** | 30-50% ↑ | CoT extrapolation |
| **Many-shot (50-100)** | 23-50% ↑ | Many-Shot ICL (2024) |
| **Prompt repetition** | 47/70 wins | Google (Dec 2025) |
| **OSST (neutralize→transfer)** | Beats baselines | arXiv:2510.13302 |
| **Persona + examples** | 15-30% ↑ | Role + ICL studies |

---

## Core Pattern: Analyze Then Apply

The single biggest lever.

```markdown
Examples of my writing:
---
[Example 1 - 300-500 words]
---
[Example 2 - different topic]
---
[Example 3 - different topic]
---

Analyze my style (quote evidence for each):
1. Sentence patterns (length, rhythm)
2. Word choice (formal/casual, favorites)
3. Punctuation (em-dashes, ellipses, parentheses)
4. Tone (hedging vs asserting, personal vs impersonal)
5. Structure (openings, transitions, closings)
6. Quirks (anything distinctive)

Then write [TASK] matching exactly.
```

**Why it works:** Explicit reasoning > implicit pattern matching. The analysis creates an intermediate representation.

---

## Prompt Repetition (Dec 2025)

Just repeat the entire prompt twice: `<QUERY><QUERY>`

- 47 wins / 70 tests, 0 losses
- One task: 21% → 97% accuracy
- No latency cost
- Neutral when reasoning enabled (CoT)

---

## OSST: One-Shot Style Transfer

Show the **transformation**, not just examples.

```markdown
NEUTRAL VERSION:
[Content stripped of style - just facts]

STYLED VERSION (my original):
[How I actually wrote it]

Apply the same transformation to:
[New neutral content]
```

**Why:** Separates content from style explicitly. One example often sufficient.

---

## Many-Shot Guidelines

| Count | Use Case |
|-------|----------|
| 3-5 | Quick test |
| 10-20 | Good consistency |
| 50-100 | Best results |

- Vary topics, keep voice constant
- Include quirks — "bad" habits are signal
- Diminishing returns beyond ~100

---

## Log-Probability Scoring

Claude doesn't expose logprobs. For OSST evaluation, use local models:

**Ollama (easiest):**
```bash
ollama pull mistral
curl http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt": "Style: [example]\nNeutral: [text]\nStyled:",
  "options": {"logprobs": true}
}'
```

Higher sum of logprobs = better style match.

**Python (Hugging Face):**
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1")
# Get log_softmax of logits for continuation tokens
```

---

## Hard Limits

| Limitation | Mitigation |
|------------|------------|
| Noun-heavy defaults | Explicit "use more verbs" |
| Discourse marker underuse | List markers to include |
| Model fingerprint | Accept ~80% ceiling |
| Very casual styles | Hardest to replicate |

---

## References

- `references/style-imitation.md` — Complete patterns, local model setup, evaluation

---

## When to Use

- Replicating your writing voice
- Style transfer between authors
- Matching brand tone
- Ghost-writing in someone's style
- Evaluating style match quality
