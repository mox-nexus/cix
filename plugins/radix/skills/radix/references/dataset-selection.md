# Dataset Selection

What to mine, in what order. Phase 2 of the radix workflow turns the user's target into a concrete dataset.

## Contents

- [Three dataset modes](#three-dataset-modes)
- [Single-source mode](#single-source-mode)
- [Collection mode](#collection-mode)
- [Domain mode — identifying elite repos](#domain-mode--identifying-elite-repos)
- [Heuristics for elite-repo identification](#heuristics-for-elite-repo-identification)
- [Sources for candidate lists](#sources-for-candidate-lists)
- [Vetting the candidate list](#vetting-the-candidate-list)
- [When to expand vs stop](#when-to-expand-vs-stop)

## Three dataset modes

The user brings a target. Read what they gave you and pick the right mode.

| User said | Mode | Setup |
|---|---|---|
| "Mine github.com/X/Y" or "this repo at /path/to/X" | **single** | Clone, mine, within-source synthesis |
| "Mine these N repos: \<list\>" | **collection** | Clone all, mine each, synthesize across the list |
| "Mine elite \<topic\> codebases" / "find expert knowledge in the \<X\> ecosystem" / "build a corpus for \<domain\>" | **domain** | Identify candidate repos, vet with user, then proceed as collection |

If the user's intent is ambiguous, ask one clarifying question: "Are you giving me (a) a specific repo, (b) a specific list of N repos, or (c) a domain you want me to find the elite repos for?"

## Single-source mode

Simplest. The user has chosen the source. Skip elite-repo identification.

- Phase 2: confirm scope (which mining modes, success criteria).
- Phase 3: extract.
- Phase 4: within-source recurrence (patterns appearing in ≥3 places within the codebase). Smaller signal than cross-source synthesis but non-empty.
- Cross-codebase principles aren't possible — flag this in `synthesis/SUMMARY.md`.

## Collection mode

The user has the list. Skip identification.

- Phase 2: confirm the list, mining modes, per-source and per-corpus success criteria.
- Phase 3: extract per source. Pick a sensible order (often: most-archaeologically-rich first, since reconnaissance benefits all subsequent passes).
- Phase 4: full cross-source synthesis. Rule of three; cross-paradigm is gold (if the collection spans paradigms).

## Domain mode — identifying elite repos

The user hasn't given a list. Build one. **Vet with them before extracting.**

The process:

1. **Articulate the domain crisply.** "Rust async ecosystem" is workable. "Programming languages" is not.
2. **Pull candidate repos** from multiple sources (see [Sources for candidate lists](#sources-for-candidate-lists) below).
3. **Score candidates** against [the heuristics below](#heuristics-for-elite-repo-identification).
4. **Present the ranked list** to the user as PLAN.md draft. Ask them to: keep / drop / add.
5. **Lock the list.** Once locked, proceed as collection mode.

Don't extract from a list the user hasn't seen. Their domain knowledge is the gate.

## Heuristics for elite-repo identification

A repo is "elite" for mining purposes when it's likely to surface stewardship-tacit knowledge that public datasets miss. Use multiple signals; no single one is sufficient.

### Strong signals (each alone earns a place)

| Signal | What to check | Why it matters |
|---|---|---|
| **High downstream-dependency rank** | libraries.io, deps.dev, package-registry stats | Many depend on it → its design choices propagate; debate around them is rich |
| **RFC presence with substantive deliberation** | `rfcs/` directory with rejected alternatives, accepted-with-modifications, multi-version RFCs | Explicit deliberation artifacts; oscillations and tradeoffs surface here |
| **Multi-year active maintenance** | Recent commits across years; multiple maintainers active | Long horizon → archaeology has accumulated; recent activity → still considered authoritative |
| **Reverts with substantive messages** | `git log --grep="revert" --pretty=full \| head` | Direct oscillation signal; if reverts are rare or terse, the repo doesn't carry this signal |
| **Battle-scar comment density** | Per language (use the markers that exist in that language's idiom — see below) | Doc comments encoding invariants — direct scar yield |

**Per-language scar density check** (run the one matching the repo's language):

```bash
# Rust / C / C++ / Go / Java / TypeScript / JavaScript (// + /* */ comment styles)
rg -c "// (SAFETY|WARNING|NOTE|XXX|HACK|FIXME|panics if|must not)" .

# Rust-specific (richest scar markers in any popular language)
rg -c "// SAFETY:|/// # Safety|// NOTE:" --type rust .

# Python (# + """ comment styles)
rg -c "# (NOTE|WARNING|TODO|FIXME|HACK|XXX):" --type py .

# Ruby (# comment style)
rg -c "# (NOTE|WARNING|TODO|FIXME|HACK):" --type rb .

# Erlang / Elixir (% and # comment styles)
rg -c "% (NOTE|WARNING|TODO):" --type erlang .

# Universal phrase-based
rg -ci "(must not|panics if|undefined behavior|unsafe to|footgun|gotcha|don't|never call)" .
```

A repo with high scar density across these markers is a strong candidate for `scars` mining; lower density doesn't disqualify it (other modes may still be rich).

### Supporting signals (combinations earn a place)

| Signal | What to check | Why it matters |
|---|---|---|
| **Cited as exemplar by other elite codebases** | Doc references, README "see also", talks/blogs | Community attestation of design quality |
| **Substantive PR discussions** | `gh pr list --state merged \| head; gh pr view <N>` for samples | If PRs have multi-paragraph review with rejected approaches, archaeology is rich |
| **CHANGELOG with breakage commentary** | `cat CHANGELOG.md \| rg -B1 -A3 -i "(breaking\|removed\|deprecated)"` | Explicit edition / migration archaeology |
| **Test density with named edge cases** | `rg "#\[test\]\|test_" \| wc -l`, sample names | Tests-as-spec; edge-case tests reveal what experts worry about |
| **Multiple issue threads with abandoned approaches** | `gh issue list --state closed --label="wontfix"` | Failure-mode reports |

### Disqualifying signals (each alone disqualifies)

| Signal | Why it disqualifies |
|---|---|
| **Single contributor, < 1 year history** | No archaeology has accumulated; tacit signal hasn't formed |
| **Trivial CHANGELOG, no RFC, no PR discussion** | Even if the code is good, there's no deliberation surface to mine |
| **Heavy auto-generated code** (LLM-output repos, codegen-only crates) | Mining produces noise; the WHO behind the code matters |
| **Vendored / fork-of-X** without independent design choices | The mining target is upstream, not the fork |

## Sources for candidate lists

When you need to *find* candidates for a domain (rather than starting from a known list):

| Source type | Where | What it gives you |
|---|---|---|
| **Package registries** | crates.io, npmjs.com, pypi.org, pkg.go.dev — sort by depended-on / downloads | High-rank repos for the language |
| **Dependency-graph services** | libraries.io, deps.dev | Cross-registry ranking + dependency trees |
| **GitHub Topics** | github.com/topics/\<topic\> sorted by stars-with-recent-activity | Community-tagged exemplars |
| **awesome-\<X\> lists** | github.com/sindresorhus/awesome → language- or domain-specific awesome list | Curated by community (variable quality) |
| **Language-specific exemplar lists** | "blessed.rs" for Rust; "awesome-go" for Go; "awesome-python" for Python; etc. | Maintainer-vetted recommendations |
| **Conference talks / blog series** | "What we learned from \<X\>" talks, postmortem blogs | Practitioner attestation |
| **Existing exemplar collections in this plugin** | `references/exemplars/<language>.md` if one exists | Pre-curated starter lists |

Pull from ≥2 sources. Cross-reference. A repo that appears in multiple lists is more likely elite than one in only one.

## Vetting the candidate list

Before extraction, present the candidate list as a draft PLAN.md to the user. The minimum information per candidate:

```markdown
## Candidate list — <domain>

| Repo | Why it's a candidate | Concerns |
|---|---|---|
| owner/repo | downstream rank: <N>; RFC density: <high/med/low>; archaeology: <years of active maintenance> | <e.g., low PR-discussion density, mostly auto-generated, fork-of-X> |
```

Ask the user to: KEEP, DROP (with reason), ADD (with rationale), or DEFER (maybe later).

Drop anything they're unsure about. Mining is bounded by goal; padding the list with marginal candidates dilutes synthesis.

## When to expand vs stop

After the initial mining of the locked list:

- If success criteria are met → stop. Phase 5.
- If the rule of three is satisfied for target patterns but no universal-class principle has emerged → stop or expand based on user goal (universal-class needs cross-paradigm coverage).
- If the Nth+1 source adds no new failure-modes-or-success-modes → stop, regardless of count.
- If the user wants "completeness" without a new criterion → push back. Mining is bounded by goal.

Expansion (adding sources mid-run) is fine when:
- A specific pattern needs cross-paradigm verification and the current list doesn't span enough paradigms
- A specific candidate principle is at exactly N=3 and one more source would lift it from "floor" to "strong"
- The user surfaces a new candidate they'd missed

Each expansion is a PLAN.md edit; record the addition with rationale. STATUS.md `## Next` reflects the new sources.
