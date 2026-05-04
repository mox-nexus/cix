# Threat Modeling: How to Actually Look

Threat modeling is the discipline of enumerating what could go wrong *before* you write the code, so the architecture defends against those things rather than getting patched around them later. NIST SSDF PW.1 requires it. Most teams skip it. A whitehat review needs to be able to do it on the spot.

This reference covers two flavors: **classical threat modeling** (STRIDE for services, LINDDUN for privacy) and **agent-specific threat modeling** (trifecta-first, tool-privilege-first, boundary-lie-first). The second is not a replacement for the first — it's what you add when the system includes an LLM.

---

## When to threat-model

- **New service or endpoint** — before writing the handler
- **New agent configuration** — before giving it tools
- **New trust boundary** — before code crosses it (MCP integration, external API, file upload)
- **Incident post-mortem** — to enumerate what *else* the same class of bug might break
- **Pre-launch review** — one last attacker-minded pass before the thing ships

The canonical timing (NIST SSDF):

> "Addressing security requirements and risks during software design (secure by design) is key for improving software security and also helps improve development efficiency."

Design-time is orders of magnitude cheaper than production-time.

---

## STRIDE — Classical Threats for Services

Microsoft's STRIDE gives you six categories. Walk every component, every data flow, every trust boundary, and ask the six questions. Most real-world findings cluster into a few of the six; coverage matters more than depth on any one.

| Letter | Threat | What the attacker achieves | Design property violated |
|---|---|---|---|
| **S** | **S**poofing | Impersonate a user, process, or system | Authentication |
| **T** | **T**ampering | Modify data or code at rest or in flight | Integrity |
| **R** | **R**epudiation | Deny having performed an action | Non-repudiation / audit |
| **I** | **I**nformation disclosure | Learn data they're not authorized for | Confidentiality |
| **D** | **D**enial of service | Make the system unavailable | Availability |
| **E** | **E**levation of privilege | Gain rights they shouldn't have | Authorization |

### How to use STRIDE on a diagram

1. Draw the system as **components** (processes, data stores, external actors) connected by **data flows**, with **trust boundaries** where data crosses from one zone of trust to another.
2. For each trust-boundary crossing, walk all six letters:
   - Can someone spoof the source?
   - Can someone tamper with the data in transit?
   - If the action is denied, can we prove who did it?
   - What could be disclosed in the payload?
   - Can the flow be flooded?
   - Does crossing this boundary gain the actor new capability?
3. Record each finding with: component, threat letter, specific mechanism, mitigation.

### STRIDE review questions (for code review)

- **S**: How is the caller authenticated at this point? What token / cert / session is checked? What happens if the check is skipped?
- **T**: Is the payload signed? Hashed? Integrity-protected in flight? At rest?
- **R**: If this action were investigated six months from now, what log would exist? Is it tamper-resistant?
- **I**: What's the most sensitive thing this code path touches? Does the error message, the response, the log, or the cache leak it?
- **D**: What input size kills this? What rate kills this? What cost dimension (CPU, memory, IO, outbound bandwidth, token budget) does the attacker control?
- **E**: If this path is exploited, what does the attacker *gain*? (If "nothing" — say so, and move on. If "root on the container" — that's the finding.)

---

## LINDDUN — Classical Threats for Privacy

The privacy-focused complement to STRIDE. Use when the system handles PII, health data, financial data, or any user data with legal obligations.

| Letter | Threat |
|---|---|
| **L** | Linkability (combining records reveals identity) |
| **I** | Identifiability (single record reveals identity) |
| **N** | Non-repudiation (user can't deny action — sometimes a *privacy* harm, e.g. forced attribution) |
| **D** | Detectability (presence of a record reveals something) |
| **D** | Disclosure of information (the classical confidentiality harm) |
| **U** | Unawareness (user doesn't know they're being processed) |
| **N** | Non-compliance (legal regime violated — GDPR, HIPAA, etc.) |

For an LLM system, LINDDUN matters at embedding-time (RAG indexes are privacy surfaces), at prompt-time (user prompts are PII), and at output-time (responses can inadvertently re-identify).

---

## Agent-Specific Threat Modeling

For any system with an LLM agent, add a second pass after STRIDE/LINDDUN. The classical frames don't cover the instruction/data confusion that defines LLM attacks.

### Step 1 — Map the trifecta legs

For the agent under review, answer three questions:

1. **Does this session ever hold private data?** Enumerate: API keys, user files, tenant data, secrets, session tokens, PII from previous tools, anything in a persistent store the agent can read.
2. **Does this session ever read attacker-influenceable content?** Enumerate: web-fetch results, email bodies, search results, RAG retrieval, tool outputs from systems with user-controlled input, PR descriptions, issue comments, filename arguments.
3. **Can this session cause a state change or outbound communication?** Enumerate: HTTP POSTs, writes to shared filesystems, database writes, webhook calls, markdown images/links that render in a way that hits a server, DNS lookups.

If **yes to all three** → the lethal trifecta is present. Design must cut a leg, use a dual-LLM pattern, or require human-in-the-loop for every consequential action. Document which mitigation applies.

### Step 2 — Enumerate tools and their blast radius

For every tool the agent can call:

| Tool | Input source (attacker-controllable?) | Effect if attacker controls input | Mitigation |
|---|---|---|---|
| (example) `web_fetch` | URL from model output | Fetch any reachable resource; leak URL as query string | Domain allowlist, inspect each allowlisted endpoint for upload surface |
| (example) `shell_exec` | Command from model output | Arbitrary code execution | Remove this tool; use specific typed tools instead |
| (example) `send_slack` | Channel + message | Post attacker content; exfiltrate via message body | Human approval before send; allowlist channels |

OWASP LLM06 is the framing:

> "Limit the extensions that LLM agents are allowed to call to only the minimum necessary."
> "Avoid the use of open-ended extensions where possible (e.g., run a shell command, fetch a URL, etc.)."

### Step 3 — Walk the indirect-injection path

For each untrusted input source:

1. Could an attacker plant instructions there?
2. Will the agent read those instructions as text entering its context?
3. What tools does the agent have available after reading that input?
4. What would those tools accomplish in the attacker's interest?

NIST AI 100-2:

> "application designers may design systems with the assumption that prompt injection attacks are possible if a model is exposed to untrusted input sources, such as by using multiple LLMs with different permissions or by allowing models to interact with potentially untrustworthy data sources only through well-defined interfaces."

Design for the injection landing. What does the architecture contain?

### Step 4 — Check the trust-boundary lie

Mudge's signature move. For every claimed security property in the system:

- "We isolate tenants." → What shares the DB? The cache? The cron job? The log index? The embedding store?
- "We rate-limit per user." → Is the rate-limit keyed on a value the user controls (IP, UA)?
- "We log all access." → Is the log path's own access logged? Can the same user who caused the event delete the log?
- "We require MFA." → Is there a break-glass path? A recovery path? A legacy-session path?

Every claim is a hypothesis. Every hypothesis is a test. If the test doesn't exist, the claim is wishful thinking.

### Step 5 — Observability before controls

Before evaluating the containment, evaluate the ability to detect:

- If this were compromised tonight, what log would tell me?
- If the log exists, who reviews it, on what cadence?
- If the log is tampered with, what detects that?
- If the log is "too noisy," what signal would make it through?

Zatko's Twitter disclosure named this as the first-order finding: no logs on production access. An unobservable system is, by definition, a system whose security claims cannot be falsified.

---

## Output Format: A Threat Model

Keep it short. A threat model that isn't read is a threat model that doesn't exist. Target 1–2 pages per subsystem.

```markdown
# Threat Model: <subsystem>

## Scope
- What this model covers
- What is explicitly out of scope

## Components + Trust Boundaries
- Diagram (or textual description)
- Trust zones named

## Assumptions
- What we assume about the environment / adversary / users

## Threats (STRIDE + agent-specific)

### T-01: <short name>
- Component: ...
- Category: S | T | R | I | D | E | Trifecta | ...
- Mechanism: ...
- Impact: ...
- Likelihood: ...
- Mitigation: ...
- Residual risk: ...

### T-02: ...

## Out-of-scope / Accepted Risks
- Things we considered and decided not to fix, with reasons
```

---

## Anti-Patterns

Threat modeling done badly is worse than not done, because it provides false confidence.

- **The security checklist masquerading as a threat model.** A list of "did you think about X?" isn't a model. It's a quiz. Real threat modeling is the *structure*: components + flows + boundaries → per-boundary walk of threats.
- **The attack tree with no leaves.** "Compromise the system → Authenticate as admin → Steal admin creds." OK, and then what? Every leaf should be a concrete, reproducible action.
- **The "we'll worry about that later" exit.** If a risk is accepted, write it down as accepted, with whose decision and why. If it isn't written down, it isn't accepted — it's ignored.
- **The threat model that never touches code.** The document and the code diverge; eventually the threat model is fiction. Tie threat IDs into test names (`test_T03_authz_bypass_...`). Make the model cost something to be wrong.

---

## Abbreviated Agent-Specific Threat Model Template

For a fast agent review where you don't have time for the full STRIDE walk:

```markdown
# Agent Threat Model: <agent name>

## Trifecta legs (circle all that apply):
- [ ] Access to private data: what? ...
- [ ] Untrusted content: from where? ...
- [ ] Outbound / state change: to where? ...

## If 3 of 3 → mitigation:
- [ ] Cut which leg? ...
- [ ] Or: human-in-the-loop for which actions? ...

## Tools inventory:
| Tool | Blast radius | Necessary? | Mitigation |
|---|---|---|---|

## Untrusted input sources:
- Source: ... → Reaches context: ... → Containment: ...

## System prompt audit:
- Secrets present: ...
- AuthZ logic present: ...
- Assume-leaked-public posture: ...

## Observability:
- If compromised tonight, which log names the incident?
```

Takes 15 minutes. Catches the majority of agent-level findings. Use it.

---

## Sources

- Microsoft STRIDE: https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats
- LINDDUN (KU Leuven): https://linddun.org/
- NIST SP 800-218 SSDF v1.1: https://csrc.nist.gov/publications/detail/sp/800-218/final
- OWASP Top 10 for LLM Applications 2025: https://genai.owasp.org/llm-top-10/
- NIST AI 100-2 E2025 (Adversarial ML): https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf
- Simon Willison, *The lethal trifecta*: https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
- Zatko Twitter whistleblower disclosure (2022), via https://www.theregister.com/2022/08/23/twitter_security_whisterblower/
