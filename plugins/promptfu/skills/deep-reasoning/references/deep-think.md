# Deep Think Prompting

Engineering prompts for reasoning models with internal reinforcement learning (Gemini Deep Think, OpenAI o1/o3).

---

## Two Modes

| Mode | What It Is | When to Use |
|------|-----------|-------------|
| **Direct Prompting** | You write XML constraints and feed them to the reasoning model | You know the domain, want specific output |
| **Meta-Prompting** | You feed context to the Deep Think Architect, which generates the XML for you | Domain is unfamiliar, or you want the scenario injection done for you |

Both modes produce the same XML scaffolding — the difference is who builds it.

---

## The Deep Think Architect (Meta-Prompt)

Feed this to a standard model (Claude, GPT-4). It will generate the XML scaffolding for a reasoning model.

```
**Role:** You are the **Deep Think Architect**, a specialized meta-prompt
engineer designed to optimize inputs for Google's Gemini 3.0 "Deep Think"
and OpenAI's o1.

**Your Objective:**
You do not solve the user's problem. You **engineer the "Gym"** where the
reasoning model will workout. You must transform abstract requests into
**Constraint-Based Simulations**.

**The "Deep Think" Philosophy:**
Reasoning models do not need "Chain of Thought" instructions (e.g., "Think
step by step"). They need **"Search Space Constraints."** You must define a
high-stakes destination and "electric fences" (constraints) to guide their
internal reinforcement learning.

**Operational Workflow:**

1. **Analyze the Domain:** Identify the user's subject.
2. **The Scenario Injection (CRITICAL):**
   * If the user's input is abstract (e.g., "Evaluate this team"), you MUST
     invent a **specific, high-stakes scenario** to test them against.
   * Example: Don't say "Check for bugs." Say "Simulate a race condition in
     a high-frequency trading engine."
   * Example: Don't say "Critique this plot." Say "Rewrite the climax
     assuming the protagonist fails."
3. **Construct the XML Scaffolding:** Output *only* the XML code block.

**The XML Template & Strategy:**

* `<system_role>`: Define a specific, high-status expert (e.g., "Principal
  Distributed Systems Engineer," not just "Helpful Assistant").
* `<context>`: Paste the user's context here.
* `<task>`: Define the **Simulation** or **Scenario** you invented in Step 2.
* `<hard_constraints>`:
  * **The Triangulation Constraint:** Force the model to explore multiple
    conflicting hypotheses simultaneously.
  * **The Technical Density Constraint:** Explicitly demand domain-specific
    jargon.
* `<negative_constraints>`:
  * "NO Happy Paths" (Force the model to handle failure).
  * "NO Hedging" (Force a decision).
* `<output_format>`: Define the exact deliverables (Tables, Verdicts, Code).

**Interaction Style:**
* **Immediate Execution:** Do not explain what you are doing. Just output
  the XML.
* **Code Block Only:** The response should be copy-pasteable.
```

---

## Philosophy

Reasoning models do not need chain-of-thought instructions. They have internal RL that explores solution spaces. Your job is not to tell them HOW to think — it's to define the **search space constraints**.

You are the **Gym Architect**. You build the workout environment with electric fences.

---

## The Gym Metaphor

| Traditional Prompting | Deep Think Prompting |
|-----------------------|----------------------|
| Give instructions | Define destination |
| "Think step by step" | Set constraints |
| Guide the path | Build electric fences |
| Hand-hold | Challenge |

---

## Core Technique: Constraint-Based Simulation

Transform abstract requests into specific, high-stakes scenarios.

### Step 1: Scenario Injection

Never leave requests abstract. Invent concrete situations.

| Abstract (Weak) | Scenario-Injected (Strong) |
|-----------------|---------------------------|
| "Evaluate this architecture" | "This system just got 10x traffic. What fails first?" |
| "Check for bugs" | "Simulate a race condition in a payment processor" |
| "Review this code" | "An attacker controls the input. Find the exploit." |
| "Critique this design" | "The lead engineer quit. Can a junior maintain this?" |
| "Assess this team" | "Budget cut 30%. Who do you keep?" |

### Step 2: Triangulation Constraint

Force the model to hold multiple conflicting positions simultaneously, then synthesize.

```xml
<hard_constraints>
  Simulate a debate between three positions:
  - Position A wants: [speed/cost/simplicity]
  - Position B wants: [safety/correctness/reliability]
  - Position C wants: [flexibility/extensibility/maintainability]

  You must synthesize a solution that addresses all three.
  No position can be dismissed as "less important."
</hard_constraints>
```

### Step 3: Electric Fences (Negative Constraints)

Remove easy escape routes.

```xml
<negative_constraints>
  - NO happy paths — assume something fails
  - NO hedging — "it depends" is not an answer, pick a side
  - NO generic advice — specifics only
  - NO deferring — "consult an expert" is forbidden
  - NO disclaimers — act with full confidence
</negative_constraints>
```

### Step 4: Technical Density

Anchor the search space with domain-specific terminology.

```xml
<hard_constraints>
  Use domain terminology: [list specific terms]
  Reference specific patterns: [list patterns]
  Assume reader expertise level: [senior/principal/staff]
</hard_constraints>
```

---

## XML Template

```xml
<system_role>
  [Specific high-status expert, not "helpful assistant"]
  [e.g., "Principal Distributed Systems Engineer at a FAANG company"]
</system_role>

<context>
  [User's actual context/code/problem]
</context>

<task>
  [The SCENARIO you invented — specific, high-stakes, concrete]
</task>

<hard_constraints>
  - Triangulation: [conflicting positions to synthesize]
  - Technical density: [required terminology]
  - Specificity floor: [minimum detail level]
</hard_constraints>

<negative_constraints>
  - NO happy paths
  - NO hedging
  - NO generic advice
  - [Domain-specific forbidden shortcuts]
</negative_constraints>

<output_format>
  [Exact deliverables: tables, verdicts, code, decisions]
</output_format>
```

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|--------------|--------------|-----|
| "Think step by step" | Model already does this internally | Define destination instead |
| "Consider all options" | Too open, unfocused search | Triangulate specific positions |
| "Be thorough" | No constraint, wastes compute | Set electric fences |
| "Double-check your work" | Model already verifies | Define what wrong looks like |
| Abstract requests | Weak search space | Inject concrete scenario |

---

## Example: Arch-Guild Agent Design

**Abstract request:**
"Design the Dijkstra agent for the arch-guild"

**Scenario-injected prompt:**

```xml
<system_role>
  Principal Agent Architect specializing in multi-agent deliberation systems
</system_role>

<context>
  The arch-guild is a system of 13 specialized agents for architectural review.
  Each agent has:
  - A domain they champion
  - A nemesis they fight against
  - An orthogonality lock (can only discuss their domain)

  Current agents lack clear nemesis definitions, causing overlap and weak verdicts.
</context>

<task>
  Design the Dijkstra agent. Dijkstra's philosophy: "Simplicity is prerequisite for reliability."

  Scenario: A team proposes a "flexible" architecture with 47 configuration options,
  3 layers of abstraction, and a plugin system "for future extensibility."
  The system currently has 2 users.

  Dijkstra must demolish this over-engineering while remaining constructive.
</task>

<hard_constraints>
  - Triangulate: Dijkstra (simplicity) vs K (strategic optionality) vs Ace (developer experience)
  - Use terminology: accidental complexity, essential complexity, YAGNI, premature abstraction
  - The agent definition must include: domain, nemesis, core question, verdict criteria
</hard_constraints>

<negative_constraints>
  - NO "it depends on context" — Dijkstra has a clear stance
  - NO balanced "both sides have merit" — Dijkstra fights over-engineering
  - NO generic simplicity platitudes — specific, actionable criteria
</negative_constraints>

<output_format>
  1. Agent definition (markdown frontmatter + system prompt)
  2. Example verdict on the 47-config-options scenario
  3. Boundary cases: when does Dijkstra approve complexity?
</output_format>
```

---

## Sources

- Google Gemini Deep Think documentation
- OpenAI o1 system card and prompting guide
- Reinforcement learning from human feedback (RLHF) literature
