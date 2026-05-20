# Classic Security Principles

**Two tiers — don't flatten them.** This is the load-bearing distinction for this reference:

- **[FORCING]** — Architectural forcing functions. When implemented correctly, the bug is *impossible to write*. Pit-of-success territory. Load these into the review flow by default. Every [FORCING] principle maps to a specific structural mechanism (language feature, library default, middleware, type system, infrastructure policy).
- **[POSTURE]** — Organizational posture. Program management, disclosure culture, executive alignment. Real and important, but **not falsifiable from a code diff**. They belong in governance documents, not in review-time checklists. A review that treats [POSTURE] as on-par with [FORCING] has confused ceremony for structure.

Every principle below is tagged. Source-grounded with direct quotes. Each has a **motivation** (why it matters) and a **review question** (what to actually ask when looking at code). [FORCING] principles also have a **structural mechanism** (the concrete thing that makes the bug impossible, not just discouraged).

## Saltzer & Schroeder (1975) — Eight Design Principles

From *The Protection of Information in Computer Systems*, Proceedings of the IEEE, Vol. 63, No. 9, §I.A.3. Available at https://www.cs.virginia.edu/~evans/cs551/saltzer/.

Framing quote:

> "Since no one knows how to build a system without flaws, the alternative is to rely on eight design principles, which tend to reduce both the number and the seriousness of any flaws." And: "these principles do not represent absolute rules — they serve best as warnings. If some part of a design violates a principle, the violation is a symptom of potential trouble, and the design should be carefully reviewed."

### 1. Economy of Mechanism [FORCING-ADJACENT]

> "Keep the design as simple and small as possible."

**Motivation (verbatim):**

> "design and implementation errors that result in unwanted access paths will not be noticed during normal use… techniques such as line-by-line inspection of software… are necessary. For such techniques to be successful, a small and simple design is essential."

**Structural mechanism:** small security kernels (seL4 microkernel approach), TCB minimization, chokepoint architecture where a single ~500-line module owns all authorization decisions. Not all smallness is security-relevant, but concentrating security decisions in a small reviewable core is.

**Review question:** *Can I reduce this surface? What code could I delete and still meet the requirement?*

### 2. Fail-Safe Defaults [FORCING]

> "Base access decisions on permission rather than exclusion."

**Motivation (verbatim):**

> "A design or implementation mistake in a mechanism that gives explicit permission tends to fail by refusing permission, a safe situation… a mistake in a mechanism that explicitly excludes access tends to fail by allowing access, a failure which may go unnoticed."

**Structural mechanism:** deny-by-default IAM policies (not deny-lists); allowlist matching (not denylist); `match` / `switch` with exhaustiveness checking (Rust, Scala, TypeScript with strict); typed tagged unions where "unknown" is a representable case you must handle. The structure forces the programmer to face the unmatched case.

**Review question:** *When the matching logic doesn't match, what happens? Does the unmatched path fail closed?*

### 3. Complete Mediation [FORCING]

> "Every access to every object must be checked for authority."

**Motivation (verbatim):**

> "It forces a system-wide view of access control, which in addition to normal operation includes initialization, recovery, shutdown, and maintenance… proposals to gain performance by remembering the result of an authority check [must] be examined skeptically."

**Structural mechanism:** all access goes through a single chokepoint (middleware, database driver, reference monitor). Parameterized queries enforce mediation at the DB boundary. Framework-level authorization middleware (Rails `before_action`, Django `@login_required`, Axum extractors with auth scope) ensures no handler can skip the check. Capability-based APIs — a function that requires an `AuthenticatedUser` type cannot be called without one.

**Review question:** *Is there an alternate code path (recovery, admin, cron, migration) that bypasses the check? What happens when authority changes — does the cached decision get invalidated?*

### 4. Open Design

> "The design should not be secret."

**Motivation (verbatim):**

> "The mechanisms should not depend on the ignorance of potential attackers, but rather on the possession of specific, more easily protected, keys or passwords."

**Review question:** *What's the secret this relies on? A key? Or the algorithm itself? If the algorithm leaks, does the security hold?*

### 4. Open Design [FORCING]

> "The design should not be secret."

**Structural mechanism:** use standard, peer-reviewed crypto primitives (TLS, AES-GCM, Argon2, Ed25519). Rely on secret *keys* that rotate, not secret *algorithms* that don't. The Kerckhoffs principle at the library level.

**Review question:** *What's the secret this relies on? A key? Or the algorithm itself? If the algorithm leaks, does the security hold?*

### 5. Separation of Privilege [FORCING]

> "Where feasible, a protection mechanism that requires two keys to unlock it is more robust and flexible than one that allows access to the presenter of only a single key."

**Motivation (verbatim):**

> "once the mechanism is locked, the two keys can be physically separated… no single accident, deception, or breach of trust is sufficient to compromise the protected information."

**Structural mechanism:** MFA *enforced at the auth layer*, not asked for politely. Quorum-based key release (HashiCorp Vault Shamir's secret sharing, AWS KMS grants with multi-party approval). Dual-control on destructive actions (prod database changes requiring two approvals in CI). Multi-party code review as a merge-gate, not a social norm.

**Review question:** *Can a single compromised credential, token, or insider cause total loss? If yes, where can we add an independent second check (MFA, dual-control, out-of-band confirmation)?*

### 6. Least Privilege [FORCING — when measured]

> "Every program and every user of the system should operate using the least set of privileges necessary to complete the job."

**Motivation (verbatim):**

> "this principle limits the damage that can result from an accident or error. It also reduces the number of potential interactions among privileged programs to the minimum for correct operation… if a mechanism can provide 'firewalls,' the principle of least privilege provides a rationale for where to install the firewalls."

**Structural mechanism:** capability-based security (return a handle, not permission to open one). Scoped OAuth tokens with narrow `scope:` claims. Short-lived credentials (minutes, not years) via STS/workload identity. Kubernetes RBAC with NetworkPolicy. IAM policies generated from observed usage (AWS Access Analyzer), not hand-written. **Without measurement of exercised-vs-granted privilege, "least privilege" becomes [POSTURE] — a claim not a structure.**

**Review question:** *What can this code/user/process do that it doesn't need to do? Why does it have those rights? What's the observed-vs-granted ratio?*

### 7. Least Common Mechanism [FORCING]

> "Minimize the amount of mechanism common to more than one user and depended on by all users."

**Motivation (verbatim):**

> "Every shared mechanism (especially one involving shared variables) represents a potential information path between users and must be designed with great care to be sure it does not unintentionally compromise security."

**Structural mechanism:** per-tenant credentials (not shared service accounts). Per-request object allocation (not shared mutable state). Process / container / namespace isolation for multi-tenant workloads. DB row-level security (PostgreSQL RLS) or tenant-per-schema. Separate Redis/caches per trust domain.

**Review question:** *What does this share across tenants/users/sessions — cache, global, DB connection, env var? Can one user's data or actions leak to another through that shared thing?*

### 8. Psychological Acceptability [FORCING — when the easy path IS the safe path]

> "It is essential that the human interface be designed for ease of use, so that users routinely and automatically apply the protection mechanisms correctly."

**Motivation (verbatim):**

> "to the extent that the user's mental image of his protection goals matches the mechanisms he must use, mistakes will be minimized. If he must translate his image of his protection needs into a radically different specification language, he will make errors."

**Structural mechanism:** this is the pit-of-success principle itself. Make the safe API the default import. Make the unsafe path require extra ceremony (`unsafe { ... }` in Rust, `# type: ignore` comments flagged in CI, `TrustedHtml::from_raw(...)` constructor signposted as dangerous). If the *easy* thing and the *safe* thing are the same thing, you have a pit of success. If they diverge, developers will route around the safe path under deadline pressure.

**Review question:** *Is the secure path also the easy path? If not, users will route around it.*

---

## CISA et al. (2023) — Secure by Design Principles

From *Shifting the Balance of Cybersecurity Risk: Principles and Approaches for Secure by Design Software*, co-authored by CISA, NSA, FBI, and 14 allied cyber agencies. Available at https://www.cisa.gov/sites/default/files/2023-10/SecureByDesign_1025_508c.pdf (portal: https://www.cisa.gov/securebydesign).

### Framing definitions

> "'Secure by design' means that technology products are built in a way that reasonably protects against malicious cyber actors successfully gaining access to devices, data, and connected infrastructure."

> "'Secure by default' means products are resilient against prevalent exploitation techniques out of the box without added charge… without end-users having to take additional steps to secure them. Secure by default is a form of secure by design."

> "Security should not be a luxury option, but should be considered a right customers receive without negotiating or paying more." (p. 9)

### The three principles (verbatim, p. 10)

**1. Take ownership of customer security outcomes.** [POSTURE]

> "and evolve products accordingly. The burden of security should not fall solely on the customer."

**Motivation:** Program management stance. If the vendor ships a product with unsafe defaults, claims the customer is "responsible for configuring it correctly," and the customer gets breached — the vendor is the root cause. Shift the cost inside the organization that can fix it at scale. Not a code-review finding; belongs in the governance doc.

**2. Embrace radical transparency and accountability.** [POSTURE]

> "Software manufacturers should pride themselves in delivering safe and secure products… a strong commitment to ensure vulnerability advisories and associated common vulnerability and exposure (CVE) records are complete and accurate."

**Motivation:** Disclosure culture. Attackers do not care about CVE accuracy when they already have exploits; downstream customers and defenders do. Important for the ecosystem, not falsifiable from a diff.

**3. Build organizational structure and leadership to achieve these goals.** [POSTURE]

> "senior executives are the primary decision makers for implementing change in an organization."

**Motivation:** Incentive design. Security outcomes reflect what teams are measured on. Not a finding.

### Secure-by-default tactics (p. 9) [FORCING]

> "A secure configuration should be the default baseline. Secure by default products automatically enable the most important security controls needed to protect enterprises from malicious cyber actors, as well as supply the ability to use and further configure security controls at no additional cost."

> "The complexity of security configuration should not be a customer problem."

**Structural mechanism:** a fresh install with zero config should survive the OWASP Top-10 attack battery. `docker run my-image` should not have telnet, FTP, or plaintext admin. `./configure && make install` should not leave world-writable directories. The default config file shipped is the safe one; hardening is subtraction of safety, not addition.

**Review question:** *What happens if nobody reads the docs? Is the out-of-box posture safe, or does safety require configuration?*

---

## CISA Secure by Design Pledge (2024)

https://www.cisa.gov/securebydesign/pledge — seven voluntary commitments. Scope: enterprise software, cloud, and SaaS (not consumer IoT). The goals most relevant to code review:

### MFA — Multi-factor authentication [FORCING — when enforced]

> "measurably increase the use of multi-factor authentication."

**Motivation:** "Multi-factor authentication is the greatest defense against password-based attacks such as credential stuffing and password theft."

**Structural mechanism:** MFA enforced at the auth layer, not offered as a setting. WebAuthn / FIDO2 hardware keys eliminate phishing in a way TOTP does not. The login endpoint refuses to issue a session without a second factor — no "MFA is strongly recommended" banner, no opt-in.

### No default passwords [FORCING]

> "demonstrate measurable progress towards reducing default passwords."

**Motivation:** "Default passwords, which CISA defines as universally-shared passwords that are present by default across a product, continue to enable damaging cyberattacks."

**Structural mechanism:** first-boot forces password setup; the product will not start until the initial password is set. Better: no shared-secret auth at all — provision via cert/key distributed out-of-band. Bootstrap credentials are unique per install and short-lived.

### Eliminate vulnerability classes [FORCING — the pit-of-success principle]

> "demonstrate actions taken towards enabling a significant measurable reduction in the prevalence of one or more vulnerability classes."

**Motivation:**

> "The vast majority of exploited vulnerabilities today are due to classes of vulnerabilities that can often be prevented at scale."

**Structural mechanism examples (verbatim from CISA):**

> "Consistently enforcing the use of parametrized queries to prevent SQL injection attacks. Adopting web template frameworks with built-in protection against cross-site scripting vulnerabilities. Developing a memory safe roadmap… Providing secure defaults for developers, such as by providing 'building blocks' of secure functions and libraries that make it impossible (or significantly more difficult) to introduce a certain class of vulnerability."

This is **the** pit-of-success principle. Every other [FORCING] principle above is an instance of it. See `references/pit-of-success-primitives.md` for the concrete substrate per language/ecosystem.

**Review question:** *Is this bug a one-off, or a sample from a class? If a class, can we eliminate the class (language feature, library, framework default) rather than fix instances?*

### Security patches [POSTURE — customer outreach]

> "measurably increase the installation of security patches by customers."

Organizational: patch uptake is about customer comms, UX, and forcing-function defaults (auto-update on by default), not about a code diff.

### Vulnerability disclosure policy [POSTURE]

> "authorizes testing by members of the public… commits to not recommending or pursuing legal action against anyone engaging in good faith efforts to follow the VDP."

Legal and policy posture. Real and important for the ecosystem, not falsifiable from code.

### Accurate CVEs [POSTURE]

> "demonstrate transparency in vulnerability reporting by including accurate Common Weakness Enumeration (CWE) and Common Platform Enumeration (CPE) fields in every Common Vulnerabilities and Exposures (CVE) record."

Reporting hygiene. Attackers do not care.

### Evidence of intrusions (observability) [FORCING — when operationalized]

> "measurable increase in the ability for customers to gather evidence of cybersecurity intrusions."

**Motivation:** "It is essential that organizations have the ability to detect cybersecurity incidents that have occurred and understand what has happened."

**Structural mechanism:** structured audit logs on every authorization decision, every privileged action, every secret access. Tamper-evident log storage (append-only, hash-chained, or write-once destinations — S3 Object Lock, Cloudflare R2 immutable). On-call runbooks that include the log query for each alert class. Zatko's Twitter disclosure's load-bearing finding was observability absence: "All engineers had access. There was no logging."

**Review question:** *If this system were compromised tonight, what log would tell me? If none, that's a P0.*

---

## NIST SP 800-218 — Secure Software Development Framework (SSDF v1.1)

From https://csrc.nist.gov/publications/detail/sp/800-218/final. Defines four practice groups; the Produce Well-Secured Software (PW) group is most code-review-relevant.

### Shift Left

> "Most aspects of security can be addressed multiple times within an SDLC, but in general, the earlier in the SDLC that security is addressed, the less effort and cost is ultimately required… This principle, known as *shifting left*, is critically important regardless of the SDLC model."

**Motivation:** Fixing design-time defects is orders of magnitude cheaper than fixing shipped defects. Secure-by-design is the strongest form of shift-left.

### PW.1 — Design Software to Meet Security Requirements

> "Addressing security requirements and risks during software design (secure by design) is key for improving software security."

Task PW.1.1: "Use forms of risk modeling – such as threat modeling, attack modeling, or attack surface mapping."

### PW.4 — Reuse Existing, Well-Secured Software

> "decrease the likelihood of introducing additional security vulnerabilities into the software by reusing software modules and services that have already had their security posture checked. This is particularly important for software that implements security functionality, such as cryptographic modules and protocols."

**Review question:** *Is this rolling its own crypto / auth / parser? If yes, why not a vetted library?*

### PW.5 — Secure Coding Practices

> "Validate all inputs, and validate and properly encode all outputs. Avoid using unsafe functions and calls. Detect errors, and handle them gracefully. Provide logging and tracing capabilities."

### PW.6 — Compiler/Build Hardening

> "Implement the 'clean build' concept, where all compiler warnings are treated as errors… Enable compiler features that randomize or obfuscate execution characteristics, such as memory location usage."

### PW.9 — Secure Defaults

> "Configure Software to Have Secure Settings by Default… reduce the likelihood of the software being deployed with weak security settings, putting it at greater risk of compromise."

### PS.1 — Protect Code Integrity

> "Protect All Forms of Code from Unauthorized Access and Tampering… Use commit signing for code repositories… Use code signing to help protect the integrity of executables."

**Review question:** *Are releases signed? Are commits signed? If supply-chain attack lands today, what's my tamper-evidence?*

---

## Consolidated review rubric

When reviewing a change, walk the [FORCING] principles in order. First "no" is the finding to name first.

### [FORCING] — load these into the review flow

1. **Class elimination:** Is this bug a one-off, or a sample from a class — and is there a language/library/framework move that makes the class impossible?
2. **Fail-safe defaults:** Does the unmatched case fail closed? Is the default deny?
3. **Complete mediation:** Is there an alternate code path (admin, cron, migration, recovery) that bypasses the chokepoint? Does a single middleware / driver / reference monitor own all access decisions?
4. **Secure by default:** What happens on a fresh install with no config? Does safety require reading docs?
5. **Least privilege (measured):** What's the observed-vs-granted privilege ratio? If you can't measure it, it's [POSTURE] not [FORCING].
6. **Separation of privilege:** Can a single compromised credential cause total loss? Where's the independent second factor?
7. **Least common mechanism:** What's shared across trust domains — cache, global, DB, env var? Can one tenant affect another?
8. **Open design:** What's the secret this relies on? A key (rotatable) or the algorithm (not)?
9. **Psychological acceptability:** Is the secure path the default path? Does the unsafe path require explicit ceremony?
10. **Observability (operationalized):** If compromised tonight, what log fires? Who reads it? Can it be tampered with?
11. **Economy of mechanism:** Is the security-critical code small enough for one reviewer to hold in their head?

### [POSTURE] — governance, not code review

Load these only when reviewing an organization's security program, not a code diff:

- Take ownership of customer security outcomes
- Embrace radical transparency and accountability
- Build organizational structure and leadership
- Security-patch outreach (unless this is shipping the auto-update mechanism itself)
- Vulnerability disclosure policy
- Accurate CVE/CWE fields

If a reviewer produces findings like *"violates radical transparency"* against a code PR, they've confused tiers. Move those to governance review.
