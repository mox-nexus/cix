# Explanation Anti-Patterns

Patterns that degrade explanation quality. Three categories: encoding failures, writing tells, and structural mistakes.

## Encoding Failures

### Modal Lock

The most common failure. You default to Door 1 — Abstraction | Universal (clean taxonomies, headers, structure). When it doesn't land, you amplify the same door instead of shifting to the next.

**How it manifests**:
- Explanation feels "organized but empty" — lots of structure, no grounding
- Reader says "I still don't get it" and you respond with more categories
- Increasing abstraction when concreteness is needed

**The fix**: Shift, don't add.

| Current lock | Reader signal | Shift to |
|--------------|--------------|----------|
| Stuck in Door 1 (Principle) | "What do I actually do?" | Door 2: concretize for a constituency |
| Stuck in Door 2 (Concretions) | "Why does this matter?" | Door 3: enable self-execution |
| Stuck in Door 3 (Ground) | "How does this fit with X?" | Door 1: connect to the universal |

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

**The fix**: Cut. Then cut more. If the explanation doesn't land in fewer words, the problem isn't encoding.

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

---

## AI Writing Tells

LLM-generated text has measurable statistical signatures (Liang et al. PNAS 2025). Readers pattern-match "AI slop" and disengage. This section is a detection and countermeasure guide.

### Hard Ban List

These words are instant LLM tells. Never use them:

| Word/Phrase | Replace with |
|-------------|-------------|
| delve | explore, examine, look at, dig into |
| tapestry | (delete — it's always metaphorical filler) |
| landscape (metaphorical) | field, area, space |
| leverage (verb) | use |
| utilize | use |
| aforementioned | this, that, the |
| meticulous | careful, thorough |
| multifaceted | complex, varied |
| it's worth noting | (delete — just state the thing) |
| this underscores | this shows, this means |
| this highlights the importance of | (delete — if it's important, the reader knows) |
| in the rapidly evolving | (delete entirely) |
| at its core | (delete — just say the thing) |
| in today's [anything] | (delete — temporal throat-clearing) |

### Soft Ban List

These words aren't wrong but signal LLM when clustered. Use sparingly, never more than one per page:

`comprehensive` `robust` `crucial` `vital` `pivotal` `innovative` `cutting-edge` `groundbreaking` `game-changer` `transformative` `state-of-the-art` `unprecedented` `holistic` `synergistic` `seamless` `furthermore` `moreover` `additionally` `consequently` `embark`

**The test**: Read the paragraph aloud. If removing the word changes nothing, it was filler.

### Grammatical Tells

LLMs overuse specific grammatical constructions at measurable rates (Liang et al. PNAS 2025). These are harder to spot than vocabulary but more damaging because they shape how the writing *feels*.

| Construction | LLM overuse rate | What it sounds like | Fix |
|-------------|-----------------|---------------------|-----|
| Present participial clauses | 2-5x | "Leveraging this framework, we can..." | Finite verb: "This framework lets us..." |
| Nominalizations | 1.5-2x | "The implementation of the system..." | Active verb: "We implemented the system..." |
| "That" clause subjects | 2.6x | "That this approach works is clear..." | Direct subject: "This approach works because..." |
| Trailing significance clauses | frequent | "...which is particularly important." | Cut. If it's important, the content shows it. |
| Synonym cycling | frequent | Using 3 different words for the same thing across 3 sentences | Pick one word. Repeat it. Repetition is fine. |

**The root pattern**: LLMs produce syntactically correct but rhythmically uniform prose. Every sentence follows the same cadence. Human writing has jagged rhythm — short declarative sentences interrupted by longer exploratory ones, fragments, restarts.

### Heading Anti-Patterns

Headings are the highest-signal text on a page. LLM heading patterns are immediately recognizable.

| Pattern | Example | Why it's a tell | Fix |
|---------|---------|-----------------|-----|
| **Declarative contrast** | "Excavation, Not Observation" | Symmetric parallel structure. Humans don't title things in balanced antithesis pairs. | "What memex digs up" or just "Excavation" |
| **Gerund + Object** | "Building Collaborative Intelligence" | Sounds like a conference talk title generator | "How we build CI" or "CI in practice" |
| **The [Abstract Noun]** | "The Architecture", "The Philosophy" | Definite article + nominalization = academic posturing | "Architecture" or "How it's built" |
| **Series of balanced pairs** | "Design, Not Configuration" / "Compose, Not Configure" / "Enable, Not Replace" | Same syntactic template repeated = generated | Vary the structure. Not every heading needs a contrast. |
| **Colon-split** | "Cognitive Effects: How AI Reshapes Thinking" | Heading + subtitle in one. Reads like a paper title. | Pick one: "Cognitive Effects" or "How AI reshapes thinking" |

**The test**: Read your headings as a list. If they all follow the same grammatical template, rewrite half of them.

### Structural Tells

These are document-level patterns that signal generation even when individual sentences are clean.

| Tell | What's happening | Fix |
|------|------------------|-----|
| Five-paragraph essay | Intro → 3 body → conclusion | Break the template. Some sections need 1 paragraph, some need 7. |
| Uniform bullet lists | Every bullet is 1-2 lines, same cadence | Vary length. Some bullets are a word. Some are a paragraph. |
| Balanced pros/cons | Exactly 3 pros, exactly 3 cons | Reality isn't balanced. If there are 5 pros and 1 con, say so. |
| Rule-of-three abuse | Every list has exactly 3 items | Sometimes 1 is enough. Sometimes 5. |
| Uniform paragraph size | Eerily consistent ~4-5 sentences per paragraph | Short punchy paragraphs, longer exploratory ones, single-sentence emphasis. |
| Perfect parallelism | Every section follows identical structure | Sections should be shaped by their content, not a template. |
| Summary conclusions | Final section restates what was already said | End with new information, a question, or a directive. Don't summarize. |
| Tricolon lists | "speed, efficiency, and reliability" | Not every list needs three items or a conjunction. |

### Tone Tells

| Tell | Fix |
|------|-----|
| Never uses contractions | Technical docs can sound human. "It's" not "It is." |
| Relentlessly positive | State limitations. Criticize when warranted. |
| Excessive hedging | "It could potentially..." — make direct statements when you know things. |
| Low information density | Every sentence should carry new information. |
| Diplomatic uniformity | Never takes a position. Everything is "balanced." | Take a stand. |
| Filler transitions | "Moving on to..." "Let's now turn to..." | Just start the next section. |

### Authenticity Tests

Run these before publishing:

**The "Could Anyone Say This?" Test**: Remove your name and context. Could this have been written by any LLM about any topic? If yes, it lacks specificity.

**The Interview Test**: If someone read this aloud in an interview, would the interviewer think they wrote it or that they prompted it? Specificity, asymmetry, and implied context signal human authorship.

**The Specific Name Test**: Does the text mention specific tools, people, papers, dates, or numbers? Or does it traffic in generalities? "Studies show..." vs "Bastani et al. (PNAS 2025, n=1,000) found 17% worse exam performance."

**Authentic voice markers**:
- Specificity (names, numbers, dates)
- Asymmetry (not everything balanced)
- Technical precision (right jargon, used correctly)
- Implied context (references shared knowledge without explaining it)
- Confidence without inflation (states things directly, no "groundbreaking")
- Irregular rhythm (sentence length varies, fragments appear)

---

## Revision Checklist

Four-pass revision. Each pass has one focus.

### Pass 1: Structure
- Does the structure serve the content, or does content serve the structure?
- Are sections shaped by what they contain, or by a template?
- Do headings vary in grammatical form?
- Would a reader scanning headings alone get a useful overview?

### Pass 2: Prose Quality
- Does every sentence carry new information?
- Are there three-word alternatives to ten-word phrases?
- Do paragraphs vary in length?
- Is the rhythm varied (short-long-short, not medium-medium-medium)?
- Are verbs active and finite (not participial, not nominalized)?

### Pass 3: LLM-Speak Detection
- Run the hard ban list. Any hits?
- Check soft ban density. More than 2 per page?
- Read headings as a list — do they follow one template?
- Check paragraph lengths — suspiciously uniform?
- Look for trailing significance clauses ("which is particularly important")
- Look for synonym cycling (3 different words for the same thing)
- Check for balanced structures (exactly N pros, exactly N cons)

### Pass 4: Voice Consistency
- Read aloud. Does it sound like a person or a press release?
- Does it take positions, or hedge everything?
- Is there specificity? Names, numbers, dates?
- Does it earn its claims, or assert them?
- Would this survive the "Could Anyone Say This?" test?

---

**Sources**: Liang et al. PNAS 2025 (LLM grammatical overuse rates), Wikipedia: Signs of AI Writing, Shankar 2025 Writing in the Age of LLMs, Nielsen Norman Group: ChatGPT and Tone, arXiv:2509.19163 Measuring AI "Slop" in Text
