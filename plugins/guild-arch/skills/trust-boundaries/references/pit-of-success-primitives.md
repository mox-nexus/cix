# Pit-of-Success Primitives

The move from "principles in reviewers' heads" to "structure that makes the bug impossible." This reference names the concrete substrate — the languages, libraries, frameworks, APIs, and infrastructure patterns that turn SBD from a slogan into a pit of success.

A pit of success is a design where **the easy path is the safe path**. If you have to remember to do X for safety, it's not a pit — it's a slope. Developers will slide off under deadline pressure. The right question for every security concern is: *what structure would make it impossible to write this bug?*

---

## Capabilities over policies

A capability is an unforgeable token that grants a specific right. You can't do the dangerous thing without holding the capability. This is structurally different from "policy says you shouldn't."

| Anti-pattern (policy) | Pit-of-success (capability) |
|---|---|
| `user.role == "admin"` check scattered across handlers | Framework-level middleware injects `AdminUser` type into handler parameter; non-admin handlers literally can't call admin actions |
| `if path.startswith("/etc/passwd"): deny` | Process runs without read permission to `/etc`; the capability doesn't exist |
| "Don't commit secrets" guidelines | Pre-commit hook (Gitleaks) + server-side push protection blocks commits containing secrets |
| "Only call internal-network APIs" | Egress firewall: external destinations return connection refused |
| "Log sensitive operations" | Infrastructure-level audit (CloudTrail, Kubernetes audit log) — the application can't skip it |

**Concrete capability primitives:**

- **Kubernetes RBAC + NetworkPolicy + PodSecurityStandards** — the pod cannot talk to the cluster API, cannot exit its namespace, cannot run as root, because the infra said no. Not a policy. A capability.
- **AWS IAM with STS short-lived credentials** — 15-minute tokens scoped to one action. The token expires before the attacker can chain it.
- **Linux namespaces / user namespaces + seccomp-bpf + `NO_NEW_PRIVS`** — process literally cannot see other users' processes, cannot make the `execve` syscall family, cannot gain new privileges. Impossible by construction.
- **WASM sandboxes (wasmtime, Wasmer)** — untrusted code runs in a sandbox that can only call explicitly imported host functions. Default: can't even `gettimeofday`.
- **gVisor / Firecracker** — kernel-level syscall filtering (gVisor) or microVMs (Firecracker) for hostile workload isolation.
- **Capsicum (FreeBSD), Pledge / Unveil (OpenBSD)** — file-descriptor-only access after `pledge()`/`unveil()`. Process cannot `open()` new files.

**Review question:** *Is the privilege enforced as a capability (held token, OS-level isolation, infra-level policy) or as a runtime check in the application?* If the latter, find the capability-level fix.

---

## Trust-typed data

Encoding trust in the type system — the compiler refuses to compile the bug.

### The idea

Instead of "remember to escape this before rendering," make the *type* of the string carry its provenance and render-safety. `UntrustedStr` cannot be passed to functions that expect `SafeHtml`. The type checker is the reviewer.

### Concrete patterns

**Newtype for tainted strings (Rust):**

```rust
pub struct UntrustedHtml(String);  // from user input
pub struct SafeHtml(String);       // after escaping

impl UntrustedHtml {
    pub fn escape(self) -> SafeHtml {
        SafeHtml(html_escape::encode_text(&self.0).into_owned())
    }
}

fn render_page(body: SafeHtml) -> Response { ... }
// render_page(user_input) // compile error: expected SafeHtml, got UntrustedHtml
```

The compiler prevents unescaped rendering. Entire class of XSS bugs becomes impossible.

**Autoescape-by-default template types:**

- **Jinja2 `Environment(autoescape=True)`** (Python) — HTML context autoescapes, explicit `|safe` filter to bypass
- **Handlebars** (JS) — `{{var}}` escapes, `{{{var}}}` does not (visible ceremony for unsafe)
- **Templ** (Go) — generates typed templates where `templ.SafeURL`, `templ.CSSClass`, etc. are required; raw interpolation refuses
- **React JSX** — all text content auto-escaped; `dangerouslySetInnerHTML` is the ceremony for unsafe (the name is the defense)
- **ASP.NET Razor** — `@model.Value` encodes, `@Html.Raw(...)` is the ceremony for unsafe

**Secret types that refuse to serialize:**

```rust
#[derive(Zeroize, ZeroizeOnDrop)]
pub struct Secret(String);

impl fmt::Debug for Secret {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Secret([REDACTED])")
    }
}

impl fmt::Display for Secret { ... same ... }

impl serde::Serialize for Secret {
    fn serialize<S>(&self, _: S) -> Result<S::Ok, S::Error> {
        Err(serde::ser::Error::custom("cannot serialize Secret"))
    }
}
```

Logging `Secret(api_key)` prints `Secret([REDACTED])`. Serializing it fails at compile-or-serialize time. Memory is zeroed on drop. The log-a-secret bug becomes impossible.

Python equivalent: Pydantic `SecretStr` — `str(s)` returns `'**********'`, `.get_secret_value()` is the explicit escape hatch.

**Language-level memory safety:**

Rust, Go, Swift, Kotlin, Java, C#, TypeScript. Entire CWE-119/120/121 (buffer overflow / stack / heap) class eliminated for code written in these languages. CISA's recommendation: "migrating to programming languages that eliminate widespread vulnerabilities."

---

## Default-deny network egress

Cut the outbound leg of the lethal trifecta at the infrastructure layer. Trying to secure this at the application layer is a losing game (Claude Cowork case: one allowlisted endpoint with upload surface = full exfiltration channel).

### Mechanisms

**Kubernetes NetworkPolicy, default-deny egress:**

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-egress
spec:
  podSelector: {}
  policyTypes: [Egress]
  egress: []  # empty = deny all
```

Plus explicit per-workload allow policies for the destinations each pod actually needs.

**VPC egress control:**

- **AWS VPC with no Internet Gateway** + VPC Endpoints for AWS services — pod can reach S3 but not `attacker.example.com`
- **Cloudflare Tunnel / Zero Trust Access** for outbound to external services — each destination is authenticated and logged
- **HTTP proxies (mitmproxy, Squid) with allowlist and inspection** — explicit list of external hosts + methods; content-type filtering

**SSRF-safe HTTP clients:**

- **Python `httpx` with custom transport** that resolves DNS and blocks RFC1918 / link-local / loopback / `169.254.169.254` (AWS metadata)
- **Go `net/http` with custom `DialContext`** for same
- The default `requests.get(user_url)` is SSRF-unsafe — wrap it or forbid direct use

**Content-type allowlisting per destination:**

For each allowed host, inspect what kinds of requests are permitted. If `api.anthropic.com` is allowlisted and accepts file uploads, it's an exfil channel. A host that only accepts `GET` requests with specific query shapes is a much smaller channel.

**Review question:** *Can the process talk to the internet at all? If yes, via which hosts, for which methods, with what content types? What gets logged?*

---

## Class-eliminating defaults per ecosystem

What to reach for. If the default is already the safe one, the team is in the pit.

### Python / web

- **SQLAlchemy ORM** or **asyncpg with `fetch(sql, *params)`** — parameterized queries by default; string-concat SQL requires ceremony
- **Jinja2 `Environment(autoescape=True)`** — HTML escape by default
- **FastAPI / Pydantic** — input validation typed at handler boundary; invalid input 422 before your code runs
- **Argon2** (via `argon2-cffi`) for password hashing — not `hashlib.sha256`
- **`secrets` module** for tokens — not `random`
- **Pydantic `SecretStr`** for API keys, passwords
- **`typer` or `click`** for CLI — no manual argv parsing
- **Avoid:** `pickle` (RCE on deserialize), `yaml.load` (use `yaml.safe_load`), `subprocess.run(shell=True)`, `eval`, `exec`

### JavaScript / TypeScript / Node

- **Prisma / Drizzle / Kysely** — typed query builders; raw SQL requires ceremony
- **React / Svelte / Vue** — JSX/template autoescape by default
- **Zod / io-ts / Valibot** for validation — types carry validation
- **`zx` / `execa`** for shell — no shell injection surface
- **`jose` / `@oslojs/crypto`** for JWT/crypto — not hand-rolled
- **TypeScript `strict: true` + `noUncheckedIndexedAccess`** — undefined-as-array-element surfaced
- **Avoid:** `eval`, `Function(...)`, `child_process.exec` with interpolation, `innerHTML =`, `dangerouslySetInnerHTML` without sanitization

### Go

- **`database/sql` with `?` placeholders** — parameterized by default
- **`html/template`** (not `text/template`) for HTML — autoescape by context
- **`crypto/rand`** (not `math/rand`) for tokens
- **`x/crypto/bcrypt`** or **`golang.org/x/crypto/argon2`** for password hashing
- **`net/http` with explicit `Timeout`** — not bare `http.Client{}`
- **Avoid:** `text/template` rendering HTML, `fmt.Sprintf` SQL, `exec.Command` with `-c`

### Rust

- **`sqlx`** with compile-time query checking — SQLi impossible at compile time
- **`askama`** or **`maud`** for templates — typed, autoescape by default
- **`argon2`** crate for password hashing
- **`rand::rngs::OsRng`** for crypto-grade randomness
- **`secrecy`** crate for `Secret<T>` wrapping
- **`zeroize`** for secure memory clearing
- **`unsafe`** is the explicit ceremony for memory-unsafe code — grep-able

### Kubernetes / containers

- **Pod Security Admission `restricted`** profile — no root, no host namespaces, seccomp enforced
- **NetworkPolicy default-deny-all** + explicit allow rules per workload
- **Non-root container images** — `USER 1000:1000` in Dockerfile; `runAsNonRoot: true`
- **Read-only root filesystem** — `readOnlyRootFilesystem: true`
- **Secrets via External Secrets Operator / SOPS / sealed-secrets** — never in manifests

### CI/CD

- **Dependabot / Renovate** — automated dep patches; fix PRs not just findings
- **Gitleaks pre-commit + GitHub push protection** — secrets can't enter history
- **Signed commits** (sigstore cosign, GPG, Git signing) — tamper-evident history
- **SLSA provenance** for build artifacts — you can verify where a binary came from
- **Pin GitHub Actions to SHA**, not tags — the `trivy-action` March-2026 compromise showed why

---

## The substrate-audit review move

Before reviewing code for bugs, audit the substrate:

1. **Language memory safety** — is this memory-safe? If not, why? (Performance claim with benchmark, vs. "we know C.")
2. **Query layer** — is SQL string-concatenation representable? If yes, it will appear eventually.
3. **Template layer** — does HTML escape by default? What's the opt-out ceremony?
4. **Secret layer** — are API keys / passwords / tokens typed as `Secret`, or as `String`? Can they serialize?
5. **Auth middleware** — is it enforced at the framework level or per-handler?
6. **Egress** — can this process reach the internet at all? What's the blast radius of compromise?
7. **Logging** — are there structured audit logs on privileged operations? Append-only storage?
8. **Deploy** — what's the Pod Security profile? Read-only root? Non-root user? Seccomp?
9. **Supply chain** — pinned deps, signed commits, SBOM, SLSA?
10. **Pre-commit** — secrets scan, lint, type check?

If the substrate is already safe, code-review findings drop by an order of magnitude. If the substrate is unsafe, code review is fighting physics.

---

## The honest observation

**Most teams can't get to a full pit of success from where they are.** Retrofitting memory safety across a million-line C++ codebase is a five-year project. Migrating from unparameterized ORMs to typed query builders is months. Adding PodSecurityStandards to existing clusters is politics as much as engineering.

So the rubric is:

- **New code / new service / greenfield:** adopt the pit-of-success primitives from day one. The cost is the same or lower than the unsafe stack, and security becomes free.
- **Existing code:** prioritize class-by-class elimination. Parameterize queries everywhere before worrying about memory safety. Pick the highest-leverage primitive first.
- **Accept what you can't fix:** if memory safety isn't achievable this year, double down on fuzzing, ASan, hardening flags, reducing TCB. Named accepted risks beat unnamed accepted risks.

The whitehat reviewer's job is not to demand perfection. It's to name which tier the team is in, which primitives they're missing, and which one change would move them up a tier. The goal is the pit, and the pit is always reachable in steps.
