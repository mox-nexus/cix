# Rubber Duck with Duck

Learning architecture decisions through Socratic dialogue.

---

## What You'll Learn

How to make better architecture decisions by thinking out loud with the Duck agent. Not getting answers—discovering them yourself through structured questioning.

## The Scenario

You're building a notification service. Users subscribe to events. When events happen, they get notified. Simple enough.

But now you need to decide: traditional CRUD with a relational database, or event sourcing?

You've read about event sourcing. It sounds powerful. But is it right here?

Instead of asking Claude "should I use event sourcing?", you bring in Duck.

## The Conversation

**You**: I'm building a notification service. Thinking about using event sourcing instead of traditional CRUD. Talk me through it?

**Duck**: Let's start here—what's driving you toward event sourcing?

**You**: Well, we need a full audit trail of what notifications were sent. Event sourcing gives us that automatically.

**Duck**: Okay, audit trail is the goal. What about your read patterns? How do you query this data?

**You**: Mostly "show me all notifications sent to user X" and "what notifications went out in the last hour."

**Duck**: Walk me through how those queries work with event sourcing.

**You**: I'd... rebuild the state by replaying events? No wait, I'd need projections. A read model that gets updated when events come in.

**Duck**: So you'd have the event stream AND a projection. What happens when requirements change and you need a different view of the data?

**You**: I'd build a new projection by replaying the event stream from the beginning. That's actually kind of powerful—I can create new views retroactively.

**Duck**: True. Now flip it—what's the team's experience with event sourcing?

**You**: We've never used it. We're comfortable with PostgreSQL and standard CRUD patterns.

**Duck**: What does that mean for velocity? For debugging when things go wrong?

**You**: Hmm. Learning curve would be steep. Debugging distributed event flows is way harder than debugging SQL queries. If something breaks at 3am...

**Duck**: Keep going—you're onto something.

**You**: If something breaks, the on-call engineer needs to understand event replay, projection consistency, eventual consistency semantics. Versus "here's a row in a table, here's the query that reads it."

**Duck**: So you've got: audit trail requirement, query patterns that need indexed access, team familiarity with CRUD, learning curve for event sourcing. What about the audit trail requirement—are there other ways to get it?

**You**: Oh. PostgreSQL has triggers. I could log every INSERT, UPDATE, DELETE to an audit table. That's... actually straightforward. And the team knows how to do it.

**Duck**: Does that solve your original problem?

**You**: Yeah. Full audit trail, queries work normally, no learning curve, operational simplicity. Event sourcing would be over-engineering for this.

**Duck**: So what's the decision?

**You**: CRUD with audit logging. Event sourcing would be cool, but it doesn't match our constraints.

## What Just Happened

Look at that progression. You started thinking "event sourcing sounds powerful." Duck didn't say "no, use CRUD." Duck asked questions:

- What are your read patterns?
- How would queries work?
- What's the team's experience?
- Are there simpler ways to solve the core requirement?

The questions exposed constraints you hadn't articulated:

- Team familiarity (operational risk)
- Query patterns (complexity of projections)
- Audit requirement (solvable without event sourcing)

You discovered the answer. Duck just held up the mirror.

## The Research Backing This

This isn't just feel-good pedagogy. The evidence is clear.

**HypoCompass pattern** (Stanford SCALE 2025): When humans evaluate AI-generated hypotheses instead of receiving solutions, debugging performance improves 12%. You're the judge, not the recipient.

**Cognitive Mirror** (Tomisu et al., Frontiers in Education 2025): AI reflects reasoning back with structured questions. This preserves the generative step—you do the thinking, Duck provides scaffolding. When you must articulate your reasoning, you engage metacognitive monitoring: detecting gaps, contradictions, assumptions.

**Mastery vs Performance orientation** (Australian Catholic University 2025): Mastery-oriented users are 35.7 times more likely to demonstrate critical thinking. Performance-oriented users ("just give me the answer") show skill degradation over time.

Duck is designed for mastery. Not dependency.

## When to Use Duck vs Mr. Wolf

This matters. They solve different problems.

| Use Duck when | Use Mr. Wolf when |
|---------------|-------------------|
| Exploring options | Something is broken NOW |
| Making architecture decisions | Stuck after multiple attempts |
| Thinking through trade-offs | Going in circles |
| You need clarity | You need the problem solved |

Duck helps you think. Wolf helps you unstick.

If you bring Duck to a production incident, you'll waste time. If you bring Wolf to an architecture decision, you'll outsource your thinking.

## What Makes This Work

The Socratic progression Duck follows:

1. What are you trying to do?
2. Why this approach over alternatives?
3. How does this work step by step?
4. What if your assumptions are wrong?
5. So what's the decision?

Each question builds on the last. By the time you reach "so what's the decision?", the answer is usually obvious.

## Try It Yourself

Next time you're making a technical decision—framework choice, architecture pattern, API design—don't ask "what should I use?"

Ask Duck: "I'm thinking X, talk me through it."

Then listen to your own reasoning. Duck will reflect it back. You'll hear the gaps. The missing constraints. The assumptions that don't hold.

That's when learning happens.

---

The goal isn't to get the right answer faster. The goal is to build the reasoning muscles that let you find right answers yourself.

Duck doesn't make you dependent. Duck makes you more capable.
