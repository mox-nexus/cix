# Debugging with the Wolf Protocol

A guided walkthrough showing how Mr. Wolf and the Wolf Protocol break debugging loops.

## What You'll Learn

By the end of this tutorial, you'll understand how the Wolf Protocol works in practice and when Mr. Wolf steps in to help.

## The Problem

You're working on a Python test that passes locally but fails in CI. The error message is cryptic.

```
FAILED tests/test_auth.py::test_token_expiry - AssertionError: expected 401, got 200
```

Your first thought: "Maybe the test setup is wrong."

## Attempt 1: Quick Fix

You adjust the test setup, changing the token expiration time from 60 seconds to 1 second.

```python
def test_token_expiry():
    token = create_token(expires_in=1)  # Changed from 60
    time.sleep(2)
    response = api_call_with_token(token)
    assert response.status_code == 401
```

Push to CI. Wait. Still fails.

```
FAILED tests/test_auth.py::test_token_expiry - AssertionError: expected 401, got 200
```

The debugging loop hook increments a failure counter silently in the background. You don't see it yet.

## Attempt 2: Another Quick Fix

"Maybe CI is caching something." You add cache clearing:

```python
def test_token_expiry():
    clear_token_cache()  # Added this
    token = create_token(expires_in=1)
    time.sleep(2)
    response = api_call_with_token(token)
    assert response.status_code == 401
```

Push. Wait. Same error.

```
FAILED tests/test_auth.py::test_token_expiry - AssertionError: expected 401, got 200
```

Failure counter: 2. Still silent.

## Attempt 3: The Loop Breaks You

"Maybe the API isn't checking expiration at all in CI." You try mocking the time:

```python
@freeze_time("2024-01-01 12:00:00")
def test_token_expiry():
    clear_token_cache()
    token = create_token(expires_in=1)

    with freeze_time("2024-01-01 12:00:03"):
        response = api_call_with_token(token)

    assert response.status_code == 401
```

Push. Wait. Same error.

```
FAILED tests/test_auth.py::test_token_expiry - AssertionError: expected 401, got 200
```

Failure counter: 3. The hook fires.

```
DEBUGGING LOOP DETECTED (3 consecutive failures). You MUST now:
1) Tell the user: 'This isn't converging. Bringing in Mr. Wolf.'
2) Spawn the `mrwolf` agent to break down the problem systematically.
Do not continue debugging yourself.
```

Claude spawns Mr. Wolf.

## Mr. Wolf Takes Over

Mr. Wolf starts with the protocol.

### Step 1: What's Actually Happening?

Mr. Wolf asks you to fill this in:

```
What I'm trying to do: Test that expired tokens return 401
What's happening instead: Test gets 200 (success) for an expired token
What I've already tried:
  - Changed expiration time to 1 second
  - Cleared token cache
  - Mocked time with freeze_time
```

Writing this down, something clicks. The test expects 401. It's getting 200. The token is being accepted when it shouldn't be.

### Step 2: Classify the Problem

Mr. Wolf identifies the type:

```
Type: Something's broken
Signs: Error message, unexpected behavior
Approach: Find the gap between expectation and reality
```

The gap: You expect the API to reject expired tokens. It's not rejecting them.

### Step 3: Route to the Right Technique

The problem type is "something's broken." Mr. Wolf routes to hypothesis-from-evidence: "What's the smallest input that reproduces this?"

You realize: you've been changing the test, not checking if the API actually validates expiration.

Mr. Wolf suggests one hypothesis:

```
Hypothesis: The API isn't checking token expiration in the CI environment.

Test: Check if the API has different configuration in CI vs. local.
```

You look at the CI environment variables. There it is:

```yaml
env:
  SKIP_AUTH_VALIDATION: true  # Left over from debugging last month
```

The API wasn't validating anything in CI.

### Step 4: One Thing at a Time

Mr. Wolf doesn't let you fix everything at once. One thing:

```
1. Remove SKIP_AUTH_VALIDATION from CI config
```

You remove the line. Push. Wait.

```
PASSED tests/test_auth.py::test_token_expiry
```

Green.

### Step 5: Verify

Mr. Wolf asks the verification questions:

```
- Does it actually work? YES (test passes)
- Did I solve the problem or work around it? SOLVED (removed root cause)
- Will this hold? YES (config persists)
```

Problem solved properly.

## The Speculative Fix Prevention Hook

Here's what would have happened if you tried to edit code earlier without evidence.

After attempt 2, you're at failure count 2. You decide to rewrite the entire token validation function.

You start editing `auth/tokens.py`. The hook fires:

```
SPECULATIVE FIX DETECTED. You're editing during active debugging
(2+ consecutive failures) without convergence. STOP and gather
evidence first:

1. Read the relevant error output and stack traces
2. Check the actual runtime state (logs, data, config)
3. Form a hypothesis based on evidence
4. THEN write the fix

Speculative fixes without evidence waste time and often introduce new bugs.
```

This would have stopped you from rewriting working code when the problem was in configuration.

## What Made the Difference

### Without Wolf Protocol (Spinning)

- Try random fix
- Push, wait
- Try another random fix
- Push, wait
- Try another random fix
- Push, wait
- Never stop to think

### With Wolf Protocol (Structured)

- Stop spinning
- Articulate what's actually happening
- Classify the problem type
- Form ONE hypothesis based on evidence
- Test the hypothesis
- Verify the solution

The protocol forces you to stop and think before you act.

## Key Takeaways

**The hook triggers at 3 failures.** Three consecutive bash commands that show error patterns trigger Mr. Wolf.

**The speculative fix hook triggers at 2 failures.** If you try to edit code during active debugging without gathering evidence first, you get warned.

**Articulation reveals gaps.** Writing down "What I've tried" often shows patterns you missed.

**One hypothesis at a time.** Testing multiple changes at once means you never know what fixed it.

**Evidence before fixes.** Read error output, check runtime state, then form hypothesis.

## When to Call Mr. Wolf Yourself

You don't have to wait for the hook. Call Mr. Wolf when:

- You've tried 2 things and neither worked
- You're trying the same approach in different ways
- You can't articulate what's actually wrong
- The problem feels like it's getting bigger, not smaller

Say: "Bring in Mr. Wolf" or "This needs Mr. Wolf."

## Practice Exercise

Next time you hit a bug:

1. Try one thing
2. If it doesn't work, try one more
3. If that doesn't work, STOP
4. Fill out the Wolf Protocol Step 1 in writing
5. Classify the problem
6. Form ONE hypothesis
7. Test it

The hardest part is stopping. The protocol works when you use it.
