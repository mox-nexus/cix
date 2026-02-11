# Evidence Verification Workflow

Practical workflow for verifying citations in explanatory content. Complements `accuracy-integrity.md` (conceptual framework) with executable steps.

## When to Verify

| Trigger | Action |
|---------|--------|
| Writing content that cites a statistic (d=, β=, n=, %, OR=) | Verify the number traces to the cited paper |
| Reviewing existing content with evidence spans | Run `verify-citations` on the article |
| Adding a new citation to bibliography | Confirm DOI resolves, paper exists, authors match |
| Claim uses "research shows" or "studies find" | Decompose: what study? what was measured? what was found? |

## Evidence Span Format

Claims backed by research use inline evidence markup:

```html
<span class="ev ev-{level}" title="{Attribution}">●</span>
```

| Level | Meaning | When to use |
|-------|---------|-------------|
| `strong` | Meta-analysis, replicated, multiple sources | d > 0.5 from meta-analysis, or 3+ converging studies |
| `moderate` | Single quality study, converging indirect evidence | One peer-reviewed study with adequate n |
| `weak` | Expert opinion, small n, preprint | Preprint, n < 50, or single unreplicated finding |
| `speculative` | Theoretical prediction, no direct evidence | Inference from adjacent domains, no direct measurement |

**Title attribution format**: `Author Year, key detail` (e.g., `Bastani 2025, n=1,000 PNAS`)

## Verification Pipeline

### 1. Bibliography Check

Every cited paper must have a bibliography entry with a DOI or URL.

```
✅ Bastani et al. (2025). "Generative AI..." PNAS. [Paper](https://doi.org/10.1073/pnas....)
❌ Bastani et al. (2025) — no URL, no DOI, unverifiable
```

Missing bibliography entries are the #1 cause of unverifiable claims. Fix bibliography first, then verify content.

### 2. Tool Verification

```bash
# Paper lookup only (no LLM, no API key needed)
uv run scripts/verify-citations.py article.md --no-llm

# With LLM grounding (needs OPENROUTER_API_KEY or VERIFY_API_KEY)
uv run scripts/verify-citations.py article.md -m google/gemini-2.0-flash-001

# Custom bibliography path
uv run scripts/verify-citations.py article.md -b path/to/bibliography.md
```

Script location: `skills/craft-explanations/scripts/verify-citations.py` (PEP 723 inline deps — `uv run` handles installation automatically).

The script extracts `<span class="ev">` claims, matches against bibliography DOIs, looks up papers via Semantic Scholar / OpenAlex, and optionally uses an LLM to check claim-abstract alignment.

### 3. Interpret Results

| Verdict | Meaning | Action |
|---------|---------|--------|
| VERIFIED | Abstract supports claim direction and magnitude | Keep, ensure attribution is precise |
| CONTRADICTED | Abstract says opposite of claim | **Fix immediately** — misrepresentation |
| PARTIAL | Paper found but no abstract or LLM skipped | Manually check paper |
| NOT FOUND | Paper not in any database | Check bibliography URL, verify paper exists |

## Common Citation Failures

From project validation (2026-02-11):

| Failure | Example | Prevention |
|---------|---------|------------|
| **Author misattribution** | β=0.507 cited as "Hemmer et al." but actually from Blaurock et al. | When NOT FOUND, check bibliography for same-year entries — the stat may belong to a different author |
| **Wrong study attributed** | OR=35.7 attributed to Lee et al. but actually from Pallant et al. | Verify specific numbers against specific papers, not summaries |
| **Outdated evidence** | 2014 aviation survey when 2025 Lancet RCT exists | Lead with the strongest, most recent evidence |
| **Wrong sample size** | "n=170 students" when study had "319 knowledge workers" | Check n, population, and design against source |
| **Preprint cited as peer-reviewed** | arXiv paper without noting preprint status | Mark evidence level as `weak` for preprints |

### Verify the Verifier

Verification tools (including this one) are also LLMs or API-dependent. When the tool reports NOT FOUND:

1. **Check local paper files** — `~/papers/` may have the actual paper text
2. **Check reference docs** — `docs/content/library/reference/` has sourced evidence summaries with DOIs
3. **Check bibliography by year** — the stat may be misattributed to the wrong author
4. **Don't remove numbers based on tool output alone** — read the source material yourself

## Bibliography Hygiene

A clean bibliography is the foundation of verifiable content.

| Check | How |
|-------|-----|
| Every citation has a bibliography entry | Match `<span>` title authors against bibliography |
| Every entry has a DOI or stable URL | DOIs preferred (`https://doi.org/10.xxxx/...`) |
| Author names match between citation and bibliography | "Lee" in citation → "Lee" in bibliography |
| Year matches | Citation year = bibliography year |
| Title is the actual paper title | Not a summary or paraphrase |

## Decision Framework

When writing explanatory content with evidence:

```
Has this claim been verified against the source paper?
├── Yes, VERIFIED → Use appropriate evidence level
├── Yes, CONTRADICTED → Remove or correct claim
├── Partially (paper found, no abstract check) → Mark as moderate, note limitation
├── No, tool says NOT FOUND
│   ├── Check ~/papers/ for paper text → may confirm the number exists
│   ├── Check reference docs for sourced evidence → may have DOI + context
│   ├── Check bibliography for same-year entries → may be misattributed to wrong author
│   └── Still can't find → Use qualitative language, mark as speculative
└── No, no time to verify → Mark as speculative, add verification TODO
```

**The rule**: Trace numbers to papers before citing. But also: trace NOT FOUND verdicts to source material before removing. Both false positives and false negatives are real.
