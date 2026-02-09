# Running a Mastery-Oriented Collaborative Coding Session

A walkthrough of building a feature using collab-scaffolds principles to maintain skill while working with AI.

## What You'll Learn

By the end of this tutorial, you'll have practiced a complete collaborative session pattern that:
- Preserves your cognitive skills while using AI
- Builds understanding, not just working code
- Identifies when you're slipping into dependency patterns
- Evaluates outcomes at three levels (task, project, system)

This is a concrete scenario. Follow along with your own feature work, or use this as a reference pattern.

## The Scenario

You're adding a new API endpoint to an existing service: `POST /api/tasks/{id}/complete` that marks a task as complete and triggers notification logic.

## Phase 1: Before Starting (5 minutes)

Before writing any code, state your intent and target quality level.

### What to do

**State the goal clearly:**

"I'm adding a task completion endpoint. It should mark the task complete, trigger notifications, and return the updated task."

**Set fidelity target:**

"This is a cobble road feature. It needs tests and error handling, but not production monitoring yet."

See the methodology guide for fidelity levels. Cobble road means: handles edge cases, has tests, but doesn't need full observability. This prevents over-engineering (building tarmac for everything) and under-engineering (shipping dirt roads to production).

### Wrong approach

Starting without a clear goal:

"Add task stuff... we'll figure it out as we go."

This leads to scope creep, unclear requirements, and wasted effort.

## Phase 2: Planning Before Code (10 minutes)

Now comes the critical step: PME friction. Planning-Monitoring-Evaluation metacognitive engagement.

### What to do

**First: Read the existing code**

Before asking AI for help, spend 10 minutes understanding what exists:

```bash
# Find the existing task model
grep -r "struct Task" src/

# Find similar endpoints
grep -r "POST /api/tasks" src/

# Understand the notification system
grep -r "notify" src/
```

This reading step is non-negotiable. Research shows that approaching AI with understanding produces 86% mastery retention. Approaching with no understanding: 39%.

**Second: Form your own approach**

Write down (in comments, scratch file, or conversation):

"I think I need to:
1. Add route handler in routes/tasks.rs
2. Update Task model with `completed_at` timestamp
3. Call notification service from handler
4. Return 200 with updated task"

This is the Planning component of PME friction. It activates metacognitive monitoring.

**Third: Present to AI**

"Here's what I'm planning. Before you generate code, does this approach make sense given the existing architecture?"

### Wrong approach

Immediately asking AI:

"Write me a task completion endpoint."

This bypasses the generative step where you build understanding. The AI generates, you accept. Your neural pathways for planning and design remain inactive. Over 3 months, this degrades architectural reasoning by 22%.

## Phase 3: Implementation (20-30 minutes)

AI generates code. Your job: comprehend it.

### What to do

**AI generates the handler:**

```rust
pub async fn complete_task(
    Path(id): Path<Uuid>,
    State(app): State<AppState>,
) -> Result<Json<Task>, StatusCode> {
    let task = app.db
        .update_task(id, |t| {
            t.completed_at = Some(Utc::now());
            t.status = TaskStatus::Complete;
        })
        .await
        .map_err(|_| StatusCode::NOT_FOUND)?;

    app.notifier.notify_completion(&task).await?;

    Ok(Json(task))
}
```

**Critical: Don't just accept it. Ask questions:**

You: "Why did you use `map_err` instead of `?` directly?"

AI: "The DB error doesn't implement `Into<StatusCode>`. The `map_err` converts it to NOT_FOUND for the HTTP response."

You: "What happens if notification fails?"

AI: "Currently, the whole request fails with 500. We could make notifications non-blocking if that's better for your use case."

You: "Yeah, task completion should succeed even if notifications fail. Let's make that fire-and-forget."

**This dialogue is the difference between 86% and 39% mastery.**

When you ask follow-up questions, you're:
- Catching design issues (notification shouldn't block)
- Building mental models (error conversion patterns)
- Maintaining cognitive engagement (not rubber-stamping)

### Wrong approach

AI generates code. You read it briefly, think "looks reasonable," and paste it in.

This is vibe coding. 17% of junior developers ship AI code with zero edits. 45% of AI code contains critical vulnerabilities. The overlap is concerning.

### Monitoring checkpoint

After implementation, pause:

"Does this match what I expected?"

If the answer is "I'm not sure what I expected," that's a warning sign. You've entered automation bias territory.

## Phase 4: Verification (10 minutes)

You're not done when it works. You're done when it's right.

### Three checks

**1. Task verification: Does it work?**

```bash
# Run the tests
cargo test complete_task

# Try it manually
curl -X POST http://localhost:3000/api/tasks/123/complete
```

This is table stakes.

**2. Project verification: Is the codebase better?**

Look at what changed:
- Is the code cleaner than what was there before?
- Did we leave any dead code or debug statements?
- Do the tests verify requirements or just implementation?

Run the cleanup check:

```bash
# Any debug statements?
grep -r "println!" src/

# Any commented-out code?
grep -r "// " src/ | grep -v "// " | head -20

# Any unused imports?
cargo clippy
```

If artifacts remain, the work isn't done.

**3. Compound verification: Is the next change easier?**

Imagine the next feature: "Add task assignment to multiple users."

With what you just built, is that easier or harder? If you followed the patterns, reused abstractions, and kept the codebase clean, it should be easier.

If you hacked around existing patterns, the next change got harder.

### Wrong approach

"It works, ship it."

This optimizes for the immediate task while degrading the system. Technical debt is a tax on every subsequent change. The 5 minutes saved today costs 50 minutes over the next month.

## Phase 5: Evaluation (5 minutes)

Crystallize what you learned.

### What to do

Ask yourself:
- "What would I do differently next time?"
- "What pattern worked that I should reuse?"
- "What did I learn about this codebase?"

Example crystallization:

"Next time: check notification patterns before implementation. We almost made task completion blocking on notifications, which would have degraded UX. Learned: fire-and-forget for non-critical side effects."

This is the Evaluation component of PME friction. It turns experience into transferable knowledge.

### Wrong approach

Finishing the task and immediately moving to the next one.

Without evaluation, each session is isolated. You don't compound learning across sessions.

## Phase 6: Watch for Anti-Patterns

These are the traps that degrade mastery:

### Vibe coding

**What it is:** Accepting AI suggestions without reading or understanding them.

**How it feels:** "AI generated it, looks reasonable, moving on."

**Why it's harmful:** 45% of AI code has critical vulnerabilities. If you don't read it, you ship vulnerable code.

**Counter:** Treat every AI suggestion as a first draft from a junior developer. You wouldn't ship junior code without review. Same standard applies.

### Avoidance crafting

**What it is:** Using AI to skip cognitively demanding work rather than amplify it.

**How it feels:** "This debugging is hard, I'll ask AI to solve it."

**Why it's harmful:** The hard parts are where learning happens. Delegating hard work atrophies the most valuable skills: architecture, debugging, design.

**Counter:** Reserve hard problems for yourself. Use AI for boilerplate and exploration, not as a crutch for difficult thinking.

### Productivity illusion

**What it is:** Believing AI makes you faster when it actually makes you slower.

**How it feels:** "I'm shipping so much code!"

**Why it's harmful:** Research shows experienced developers are 19% slower with AI but perceive themselves as 24% faster. That's a 43-percentage-point miscalibration gap. You can't trust your intuition here.

**Counter:** Measure actual time to completion, including:
- Prompting and clarification time
- Code review time
- Debugging AI-generated code
- Integration time

Track tasks with and without AI. Let data override feelings.

## The Complete Pattern

When you put it all together:

1. State goal and fidelity level before starting
2. Read existing code and form your own approach
3. Present approach to AI before asking for code
4. Ask follow-up questions about generated code
5. Monitor: "Does this match what I expected?"
6. Three verifications: task, project, compound value
7. Evaluate: "What would I change next time?"
8. Watch for anti-patterns: vibe coding, avoidance, productivity illusion

This pattern takes 50-60 minutes for a feature that might take 40 minutes with pure AI generation.

That extra 10-20 minutes is the investment in maintaining your capability. It's the difference between:
- 86% mastery retention vs 39%
- Building mental models vs building dependency
- Compounding skill vs degrading skill

## Next Steps

- Try this pattern with your next feature
- Pay attention to monitoring checkpoints
- Notice when you're tempted to skip steps
- Measure: track actual completion time with awareness vs without

The pattern feels slower at first. That's the friction working. Over time, the compounding understanding makes you genuinely faster.

## Further Reading

- `/docs/explanation/methodology.md` - Research behind these principles
- `/skills/collaboration/references/behavioral-awareness.md` - Anti-patterns in depth
- `/skills/collaboration/references/productivity-reality.md` - Evidence on AI-assisted development
