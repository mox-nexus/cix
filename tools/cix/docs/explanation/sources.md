# Sources

Research and evidence behind the cix package manager design.

---

## Research Synthesis

The evidence base for cix draws from two streams: the collaborative intelligence thesis (AI should amplify, not replace human capability) and package management history (CPAN through Nix). These converge on a design principle — cognitive extensions need the same lifecycle management as software dependencies, but with complementary design constraints that prevent skill atrophy.

---

## Collaborative Intelligence Thesis

**Hemmer, P., Schemmer, M., Riefle, L., Vossing, M., & Kuehl, N. (2024). "Complementarity in Human-AI Collaboration." European Journal of Information Systems.**

Establishes that complementary AI design -- where human and AI capabilities combine -- produces outcomes neither achieves alone. Substitutive design (AI replaces human effort) degrades human capability over time.

**Relevance to cix:** The fundamental filter for the extension ecosystem. Every extension must be complementary by design.

---

**Blaurock, M., Buttgen, M., & Schepers, J. (2025). "Designing Collaborative Intelligence Systems for Employee-AI Service Co-Production." Journal of Service Research, 28(4), 544-562.**

Two scenario-based experiments (n=654) establishing effect sizes:
- Process Control: beta = 0.507 (strongest predictor)
- Transparency: beta = 0.415
- Engagement features: b = -0.555 (negative for frequent users)

**Relevance to cix:** Extensions that maximize user control and transparency are prioritized. Engagement features (gamification, nudges) are actively discouraged.

---

**Lee, H.P., et al. (2025). "The Impact of Generative AI on Critical Thinking." CHI 2025.**

Large-scale study (n=1,505): AI confidence negatively correlates with critical thinking enacted (beta = -0.69, p&lt;0.001). Higher self-confidence in own abilities correlates with maintained critical thinking.

**Relevance to cix:** Extensions must build user confidence in their own judgment, not in the AI. This informs the mastery-over-performance design orientation.

---

## Package Management Precedent

**Nix Package Manager. "NixOS/nixpkgs: Nix Packages Collection." GitHub.**

Nix pioneered declarative, reproducible package management with channel-based sources (like cix's source model). The channel concept -- user-selected repositories of packages -- avoids central registry dependency.

**Relevance to cix:** The source-based model draws from Nix channels and Homebrew taps: decentralized discovery, user-controlled trust.

---

**The Homebrew Project. "Homebrew: The Missing Package Manager for macOS."**

Homebrew's "tap" system lets users add third-party repositories of formulae. This decentralized model enables community growth without gatekeeping while maintaining a curated default tap.

**Relevance to cix:** cix sources follow the same pattern -- a default marketplace plus user-addable sources.

---

## Hexagonal Architecture

**Cockburn, A. (2005). "Hexagonal Architecture (Ports and Adapters)." alistair.cockburn.us.**

Ports and adapters separate domain logic from infrastructure. The domain defines what it needs (ports); adapters provide how.

**Relevance to cix:** The TargetPort abstraction means cix can install to Claude Code, Cursor, or any future target. RepositoryPort means sources could be git, HTTP, or local directories. Architecture enables evolution without rewrites.

---

## Extension Design Research

**Bastani, H., et al. (2025). "Generative AI without Guardrails Can Harm Learning." PNAS.**

RCT (n=1,000): GPT Tutor (hints only) produced no learning harm. GPT Base (direct answers) caused 17% worse exam performance. Same technology, different design philosophy, opposite outcomes.

**Relevance to cix:** The extension quality evaluation criteria. Extensions that give direct answers score lower than those providing reasoning frameworks. Design philosophy determines impact.

---

**Mozannar, H., et al. (2024). "Reading Between the Lines: Modeling User Behavior and Costs in AI-Assisted Programming." CHI 2024.**

Developers spend only 22.4% of coding time verifying AI suggestions. Verification behavior is the strongest predictor of code quality outcomes.

**Relevance to cix:** Extensions should encourage verification, not bypass it. The ecosystem design principle: make verification natural, not effortful.

---

## Design Principles

**Martin, R.C. (2017). "Clean Architecture: A Craftsman's Guide to Software Structure and Design." Prentice Hall.**

The Dependency Rule: source code dependencies must point inward. Domain knows nothing of adapters. Adapters know about domain.

**Relevance to cix:** Domain models (Source, Package, Extension) have zero infrastructure imports. CLI, git, and filesystem are adapters that depend on the domain, never the reverse.
