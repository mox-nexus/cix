# Provenance & Chain of Verification

Making claims traceable and verifiable.

## Evidence Tiers

| Level | Definition | Example |
|-------|------------|---------|
| **Strong** | Multiple peer-reviewed sources, triangulated | "β = 0.415 (Blaurock meta-analysis, 106 studies)" |
| **Moderate** | Single quality source or converging evidence | "PostgreSQL + pgvector is production standard" |
| **Weak** | Expert opinion or theoretical prediction | "This pattern should scale to 1M records" |
| **Speculative** | Reasonable inference, no direct evidence | "Based on similar systems, expect..." |

## Stating Uncertainty

**Good:**
```markdown
RRF improves recall from 0.72 to 0.91 over BM25 alone (Strong: multiple benchmarks).

This architecture should handle 100K fragments (Moderate: based on DuckDB benchmarks,
not tested at this specific scale in this codebase).
```

**Bad:**
```markdown
RRF is better.
This architecture scales.
```

---

## Chain of Verification (CoVE)

Reduces hallucination by 50-70%.

### The Pattern

1. **Generate** initial claim
2. **Plan** verification questions targeting specific claims
3. **Answer** each question **independently** (no access to original)
4. **Synthesize** corrections

### Example

**Claim:** "Use pgvector for semantic search at scale."

**Verification questions:**
- What scale does pgvector support?
- What are pgvector's limitations?
- What alternatives exist and when are they better?

**Independent answers:**
- pgvector: ~1M vectors efficiently, struggles >10M
- Limitations: No HNSW until recently, filter performance
- Alternatives: Qdrant/Weaviate for >50M, complex filtering

**Corrected claim:** "Use pgvector for <50M vectors. Consider Qdrant/Weaviate for larger scale or complex filtering requirements."

---

## Source Attribution

### In Skills

```markdown
### Error Handling

Use `thiserror` for library errors, `anyhow` for applications.

**Why:** thiserror derives std::error::Error with zero runtime cost.
anyhow provides context chaining but hides the error type.

**Source:** Rust API Guidelines, tokio/reqwest usage patterns.
```

### In References

Full bibliography at end:

```markdown
## Sources

- Blaurock et al. (2024). AI-Based Service Experience. JSR. Meta-analysis of 106 studies.
- Lee et al. (2025). Generative AI and Critical Thinking. CHI 2025.
- PostgreSQL pgvector. https://github.com/pgvector/pgvector
```

---

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| **Confidence theater** | Asserting without evidence | State uncertainty level |
| **Source laundering** | Citing without verifying | Check primary sources |
| **Precision theater** | False precision on uncertain claims | Use appropriate hedging |
| **Appeal to authority** | "Experts say" without specifics | Name sources, cite studies |

---

## Applying to CI Development

### In Skills

Every recommendation should have:
- The claim (what you're recommending)
- The reasoning (why)
- The evidence tier (how confident)
- The source (where this comes from)

### In Tools

Every error should include:
- What went wrong
- Why it's a problem
- How to fix it
- (Optional) Where to learn more

### In Agents

Reasoning traces should show:
- What was observed
- What was concluded
- Confidence level
- What would change the conclusion
