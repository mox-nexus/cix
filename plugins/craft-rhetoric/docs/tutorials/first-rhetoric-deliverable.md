# Your First Rhetoric Deliverable

Write an explanation doc from start to finish using the rhetoric pipeline. By the end, you will have a shipped piece of content that passed the propagation test -- a reader can explain it to someone else, not just repeat it.

**Time:** 20-30 minutes
**What you'll produce:** A short explanation doc (like a README section or an internal "how X works" page)
**What you'll learn:** Discourse, inventio, voice checking, critique -- the core pipeline without the optional steps

## Pick something to explain

Choose something you understand well and need to document. Concrete examples:

- How your team's deployment pipeline works
- Why you chose a specific database for a project
- How a module in your codebase handles authentication

The subject should be something where *you* are the expert. The pipeline draws out what you know -- it doesn't generate knowledge for you.

For this tutorial, we'll use the example: "How our caching layer works and why we built it this way."

## 1. Set up the workspace (2 minutes)

```bash
mkdir -p .rhet-caching/{ground,inventio,critique}
echo '.rhet-*/' >> .gitignore
```

We skip `map/`, `memoria/`, `arrangement/`, `figures/`, and `staging/` because this is a single technical explanation -- no source survey, no weaving, no collection architecture, no visual artifacts, no experience design.

## 2. Run discourse (10 minutes)

Tell Claude what you want to write:

> "I want to write an explanation of how our caching layer works and why we built it this way. Load the discourse skill and help me work through it."

Claude will walk you through the three movements. Here is what the conversation looks like:

### Movement 1 -- Communicate

Claude asks: *"What are you trying to communicate? What's the core thing?"*

You might say: "Our caching layer sits between the API and the database. It uses write-through with a 5-minute TTL. The non-obvious part is why we chose write-through over write-back -- we had a consistency bug in production that cost us 3 hours of bad data."

Notice: you said the specific thing (write-through, 5-minute TTL, 3-hour incident). That specificity is your voice. Claude will note it.

### Movement 2 -- Setup

Claude asks: *"Who is this for? Where does it live?"*

You: "New engineers joining the team. It lives in our internal docs. They need to understand the caching layer in their first week because they'll touch it immediately."

### Movement 3 -- Substance

Claude asks deeper questions. This is where discourse earns its keep:

- *"What has to hold for write-through to be the right choice here?"* -- probes assumptions
- *"How would someone who prefers write-back argue against this?"* -- tests from other angles
- *"What was actually measured during that incident? 3 hours of bad data -- what did 'bad' mean?"* -- grounds in evidence

You answer. Claude captures your answers. By the end, `ground-truth.md` exists in your workspace with what you said -- not what Claude rephrased.

Claude also captures `voice.md`: maybe you use short sentences for emphasis, you cross between infrastructure metaphors and cooking analogies, you tend to understate problems ("a consistency bug" when it was a P1 incident). These are voice features to protect.

### Choosing a template

For a technical explanation, Claude will suggest the Diataxis explanation format or walk through sections freehand. Since this is a "why does X work this way?" doc, it fits the explanation format naturally. Each section becomes a file in `ground/`:

```
ground/
├── what-it-does.md
├── why-write-through.md
├── the-incident.md
└── tradeoffs.md
```

## 3. Write PLAN.md (1 minute)

```markdown
## Unit 1: Caching layer explanation

Pipeline: feynman → orwell → ebert
Sources: ground/
Entry door: Door 3 (ground — start with the concrete system)
Format: Explanation (Diataxis)
```

No sagan (this is technical content, not conviction writing). No magellan (you are the source). No tufte/jobs (no visuals or staging needed).

## 4. Launch feynman (5 minutes)

Tell Claude to run the inventio step:

> "Run feynman on the caching layer explanation. The workspace is .rhet-caching/."

Feynman reads `ground-truth.md`, `voice.md`, and the `ground/` files. Because you are the source (not papers), the comprehension transform is lighter -- feynman verifies its understanding against your ground truth rather than doing four-pass reading of external sources.

Feynman enters through Door 3 (the concrete system -- your actual caching layer) and threads the other doors:

- **Door 3 (Ground):** "The caching layer sits between the API gateway and PostgreSQL. Every read hits Redis first. Writes go to both Redis and Postgres synchronously."
- **Door 1 (Principle):** "Write-through trades write latency for read consistency. The invariant: a cache hit always returns data that matches the database."
- **Door 2 (Constituency):** "For a team of 4 shipping features weekly, the 3-hour incident taught us that debugging stale data costs more than the write latency penalty."

The draft goes to `inventio/`.

If feynman can't explain *why* write-through maintains the invariant, the gap-state tracking catches it: "GAP: I don't understand how the TTL interacts with write-through -- if a write-through fails, does the TTL cause a stale read?" Feynman flags this and asks you.

## 5. Voice check with orwell (3 minutes)

> "Run orwell on the inventio draft."

Orwell reads `ground-truth.md` and `voice.md`, then reviews the draft.

Mechanical checks first: grep for LLM tells, count em dashes, check sentence openers. Then the four-pass review.

Orwell might find:

- **Hard ban hit:** Line 12 uses "utilize" -- replaced with "use"
- **Grammatical tell:** Lines 8-11 all open with present participial clauses ("Leveraging Redis...", "Ensuring consistency...") -- rewritten as finite verbs
- **Voice drift:** Ground truth says "a consistency bug" (understated). Draft says "a critical production incident" (inflated). Orwell restores the understatement.
- **Authenticity pass:** The cooking analogy from discourse ("write-through is mise en place -- everything prepped before service starts") survived. Good.

Orwell fixes the clear issues, flags borderline cases, and reports.

## 6. Critique with ebert (3 minutes)

> "Run ebert on the voice-checked draft."

Ebert reads `ground-truth.md` first -- what was this trying to do? Then evaluates:

**Propagation test:**
- Can a new engineer explain the caching layer to another new engineer? Not just "we use Redis" but "we use write-through because of a specific incident, and the invariant it protects is..."
- Can they apply it? If they encounter a new caching decision, do they know *how to think about it*, not just what we chose?

**Three Doors check:**
- Door 1 (principle): write-through invariant -- present
- Door 2 (constituency): team context, incident cost vs. latency cost -- present
- Door 3 (ground): specific TTL, specific system, specific incident -- present
- Shift: the moment the reader crosses from "here's how it works" to "here's why it has to work this way" -- present at the incident section

**Verdict: SHIP** or **RETURN**.

If RETURN: "The propagation test fails on the TTL section -- the reader learns *what* the TTL is (5 minutes) but not *why* 5 minutes instead of 1 or 30. Return to feynman to thread Door 2 (what was this chosen against?) into the TTL paragraph."

On return, you re-run feynman on that section, then orwell, then ebert again. Max 2 returns.

## 7. Ship it

On SHIP, move the final draft from the workspace to its destination:

```bash
cp .rhet-caching/inventio/caching-layer.md docs/architecture/caching.md
```

Clean up:

```bash
rm -rf .rhet-caching/
```

Done. The explanation doc exists in your repo, passed the propagation test, and sounds like you wrote it -- because you did. The pipeline handled the delivery craft.

## What you just did

The Five Canons, applied:

| Canon | What happened | Agent |
|-------|---------------|-------|
| **Discourse** | You articulated what you know. Claude drew it out. | socrates (main Claude) |
| **Inventio** | Feynman comprehended your ground truth and drafted with all three doors. | feynman |
| **Elocutio** | Orwell stripped LLM tells and preserved your voice. | orwell |
| **Critique** | Ebert tested whether understanding actually propagates. | ebert |

You skipped Memoria (sagan -- not needed for technical content), Cartography (magellan -- you were the source), Dispositio (vyasa -- single deliverable), and Actio (tufte/jobs -- no visuals or staging).

## Next steps

- **Add sources:** If your explanation needs external evidence (papers, benchmarks), add magellan before feynman to survey them
- **Add weaving:** For essays or conviction content, add sagan after feynman's voice check to make understanding stick across audiences
- **Add visuals:** Leave `[FIGURE: cache hit/miss flow]` placeholders in the draft, then run tufte to fill them
- **Full pipeline:** See [run-pipeline-for-essay](../how-to/run-pipeline-for-essay.md) for the complete flow with all optional steps
