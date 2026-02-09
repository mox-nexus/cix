# Explanation Anti-Patterns

Patterns that degrade explanation quality. Three categories: encoding failures, writing tells, and structural mistakes.

## Encoding Failures

### Modal Lock

The most common failure. You default to principle + pattern (clean taxonomies, headers, structure). When it doesn't land, you amplify the same mode instead of shifting.

**How it manifests**:
- Explanation feels "organized but empty" — lots of structure, no grounding
- Reader says "I still don't get it" and you respond with more categories
- Increasing abstraction when concreteness is needed

**The fix**: Shift, don't add.

| Current mode | Reader signal | Shift to |
|--------------|--------------|----------|
| Principle-heavy | "What do I actually do?" | Practice — concrete example |
| Pattern-heavy | "Why does this matter?" | Principle — connect to what they care about |
| Practice-heavy | "How does this fit with X?" | Pattern — show relationships |

### Sequential Traversal

Organizing explanations as "first the theory, then the application, then the steps." This forces the reader through your sequence instead of letting them pull what they need.

**How it manifests**:
- Sections labeled "Theory", "Application", "Practice"
- Reader must read everything to find what they need
- Each section only serves one audience

**The fix**: Encode simultaneously. Every section carries all three dimensions. The reader enters through whichever door matches their need.

### Adding Instead of Shifting

When a dimension is missing, bolting on a new section instead of re-encoding what's already there.

**How it manifests**:
- Abstract explanation followed by "Practical Examples" appendix
- Theory section with a "Why This Matters" box bolted on
- Steps followed by "Understanding the Theory Behind This"

**The fix**: Don't add sections. Re-encode the existing content through the missing dimension. The theory IS the example. The steps ARE the principle.

### Explanation Inflation

Using more words when fewer would serve. Often triggered by uncertainty — when you're not sure the explanation landed, you add more rather than making what's there sharper.

**How it manifests**:
- Same point made three times in slightly different words
- Qualifiers and hedges padding every statement
- Introductions that restate what the heading already says

**The fix**: Cut. Then cut more. If the explanation doesn't land in fewer words, the problem isn't length — it's encoding.

### Confidence Theater

Projecting certainty without evidence. The explanation sounds authoritative but the claims aren't grounded.

**How it manifests**:
- "Research shows..." without citation
- "Best practice is..." without context
- Strong claims with no evidence level stated

**The fix**: Label evidence levels explicitly.

| Level | Language | Meaning |
|-------|----------|---------|
| Strong | "Research consistently shows..." | Multiple replicated studies |
| Moderate | "Studies suggest..." | Several studies, not yet definitive |
| Weak | "One study found..." | Single finding, needs replication |
| Speculative | "In principle..." | Theory only, no direct evidence |

## AI Writing Tell-Tales

LLM-generated text has measurable statistical signatures. Readers pattern-match "AI slop" and disengage.

### Vocabulary Red Flags

| Tier 1: Instant tells | Replace with |
|----------------------|--------------|
| delve | explore, examine, look at |
| leverage | use |
| tapestry | (delete) |
| robust | strong, reliable, solid |
| utilize | use |
| aforementioned | this, that, the |
| meticulous | careful, thorough |

**Tier 2**: cutting-edge, groundbreaking, innovative, revolutionary, game-changer, transformative, state-of-the-art, unprecedented

**Tier 3 (filler)**: crucial, pivotal, paramount, fundamental, essential, significant, comprehensive, holistic, synergistic, seamless

### Structural Tells

| Tell | What's happening | Fix |
|------|------------------|-----|
| Rule-of-three abuse | Every list exactly 3 items | Vary rhythm. Sometimes 1 is enough. Sometimes 5. |
| Uniform paragraphs | Eerily consistent paragraph sizes | Short punchy paragraphs, longer exploratory ones, single-sentence emphasis |
| Excessive bold | Every **key term** mechanically **bolded** | Emphasis should be rare and meaningful |
| Em-dash overuse | "This solution — unlike X — delivers" | Natural placement, not formulaic |
| Generic openings | "In today's fast-paced world..." | Start with substance. Cut the throat-clearing. |

### Tone Tells

| Tell | Fix |
|------|-----|
| Never uses contractions | Technical docs can sound human |
| Relentlessly positive | State limitations. Criticize when warranted. |
| Excessive hedging | Make direct statements when you know things |
| Low information density | Every sentence should carry new information |

### The Human Test

Before publishing:
- Could only you have written this?
- Does it reflect specific experience or knowledge?
- Are there numbers where there could be? (Numbers > adjectives)
- Does it have natural rhythm or mechanical uniformity?

---

**Sources**: Wikipedia: Signs of AI Writing, Shankar (2025) Writing in the Age of LLMs, Nielsen Norman Group: ChatGPT and Tone, arXiv:2509.19163 Measuring AI "Slop" in Text
