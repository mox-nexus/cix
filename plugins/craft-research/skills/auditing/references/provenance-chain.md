# Provenance Chain — Reference

Extended reference for end-to-end provenance tracing in research outputs.

---

## Why Provenance

Research without provenance is opinion with citations. The chain exists so that any reader can:

1. Read a finding
2. See which claims support it
3. Check those claims were verified
4. Read the exact source quotes
5. Find those quotes in the original papers

If any link breaks, the reader has no way to evaluate the finding independently. They must trust the pipeline — and trust without verification is the failure mode research exists to prevent.

---

## Chain Structure

### Layer 1: Source

The original paper, report, or dataset. Identified by:
- Author(s), title, venue, year
- DOI or stable URL
- Source tier (1-Gold, 2-Silver, 3-Bronze)

### Layer 2: Extraction

Per-source claim files in `.research/extraction/`. Each claim has:
- **Claim ID**: `[source-short-name]:c[N]` — unique, persistent
- **QUOTE**: Verbatim text from source
- **LOCATION**: Where in the source (section, page, paragraph)
- **CLAIM**: Atomic statement derived from the quote
- **TIER**: Source tier inherited from source metadata

### Layer 3: Verification

Per-source verification files in `.research/verification/`. Each claim has:
- **Verdict**: VERIFIED / CORRECTED / REFUTED / INSUFFICIENT
- **Evidence**: Independent verification findings
- **Corrected claim** (if CORRECTED)
- **Refutation** (if REFUTED)

Only VERIFIED and CORRECTED claims pass to synthesis.

### Layer 4: Synthesis

Per-question synthesis files in `.research/synthesis/`. Each finding has:
- **CLAIM**: Integrated finding
- **EVIDENCE**: List of verified claim IDs with brief descriptions
- **CONFIDENCE**: HIGH / MEDIUM / LOW / INSUFFICIENT

### Layer 5: Audit

The audit report in `.research/audit/report.md`. Traces chains and assigns verdict.

---

## Claim ID Persistence

Claim IDs are assigned at extraction and persist through the entire pipeline:

```
Extraction:    [blaurock2025:c1] — extracted
Verification:  [blaurock2025:c1] — VERIFIED
Synthesis:     Finding 1 cites [blaurock2025:c1]
Audit:         Chain for [blaurock2025:c1] ✓
```

Never rename or reassign claim IDs. If a claim is CORRECTED, the ID stays the same — the corrected text is recorded alongside the original.

If a claim is REFUTED, the ID stays — it's marked REFUTED and excluded from synthesis, but the record persists for the audit trail.

---

## Worked Audit Example

### Finding Under Audit

```
FINDING: User control is the strongest predictor of human-AI
         co-production quality (β=0.507).
EVIDENCE: [blaurock2025:c1], [lee2024:c3], [wang2023:c7]
CONFIDENCE: HIGH
```

### Chain Walk: [blaurock2025:c1]

**Step 1: Synthesis → Verification**

Check `.research/verification/blaurock2025.md`:
```
### [blaurock2025]:c1 — VERIFIED
ORIGINAL CLAIM: User control has the strongest effect on
  co-production quality (β=0.507, p<0.001)
VERIFICATION: Confirmed. Source states "user control had
  the strongest effect on co-production quality
  (β=0.507, p<0.001)" in Results section.
```
✓ Verification record exists, verdict is VERIFIED.

**Step 2: Verification → Extraction**

Check `.research/extraction/blaurock2025.md`:
```
### [blaurock2025]:c1
QUOTE: "user control had the strongest effect on
  co-production quality (β=0.507, p<0.001)"
LOCATION: Results, Section 4.2, paragraph 1
CLAIM: User control has the strongest effect on
  co-production quality (β=0.507, p<0.001)
TIER: 1
```
✓ Extraction record exists with verbatim quote and location.

**Step 3: Extraction → Source**

Open the source paper (Blaurock et al., 2025). Navigate to Results, Section 4.2, paragraph 1. Find the quote.

✓ Quote exists verbatim at the claimed location.

**Step 4: Cross-Check**

- β=0.507 in finding matches extraction matches source? ✓
- "strongest predictor" — is this what the source says? Source says "strongest effect" ✓
- Scope: finding says "human-AI co-production quality" — source says "co-production quality" — acceptable ✓
- Confidence HIGH: 3 sources with RCT — warranted ✓

**Result**: Chain intact. Finding is grounded.

### Chain Walk: [lee2024:c3]

Follow the same process for the second evidence source...

---

## Common Chain Breaks

### The Telephone Break

```
Source: "associated with improved outcomes (r=0.34)"
Extraction: "improves outcomes (r=0.34)"
Verification: VERIFIED (verified r=0.34)
Synthesis: "causes improved outcomes"

Break: causal inflation at synthesis layer
```

The verifier checked the number (correct) but the synthesizer changed the causal language. Each layer introduces small distortions that compound.

### The Missing Link

```
Synthesis: Finding cites [study:c5]
Verification: No record for [study:c5]

Break: claim was never verified
```

The claim entered synthesis without passing through verification. This can happen when extraction produces claims that the synthesizer uses directly.

### The Ghost Quote

```
Extraction: QUOTE: "significant improvement of 23%"
Source: Quote not found at claimed location

Break: quote is fabricated or from a different source
```

The extraction contains a quote that doesn't exist in the source. Could be hallucinated, from a different paper, or from a version that was updated.

### The Scope Creep

```
Source: Tested on English-language tasks only
Extraction: [correctly notes English-only]
Verification: VERIFIED
Synthesis: "Across languages, X improves Y"

Break: synthesis dropped the scope limitation
```

Each layer is faithful, but the synthesis overgeneralizes beyond what the sources support.

---

## Audit Sampling Strategy

### For the Auditor

You cannot verify every chain in a large synthesis. Sample intelligently:

1. **All HIGH-confidence findings**: These are your strongest claims. 100% chain verification.
2. **All key numbers**: Any number that appears in the executive summary or would be cited. 100%.
3. **Random sample of MEDIUM findings**: 50%. Checks for systematic errors.
4. **Random sample of LOW findings**: 25%. Already flagged as weak.
5. **Any finding that "feels right"**: Confirmation bias check. Verify what seems obvious.

### Red Flags to Escalate

- Multiple rounding errors → systematic extraction problem
- Multiple scope inflations → systematic synthesis problem
- Multiple rubber-stamp verifications → verification wasn't independent
- Any fabricated quote → stop audit, return to extraction for full re-check
