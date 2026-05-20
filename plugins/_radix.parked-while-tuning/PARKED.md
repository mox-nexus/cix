# radix — parked while tuning

This plugin is **intentionally parked** while the radix skill is being iterated on as a local fork inside the rust-mastery workspace. It is **not registered in the cix marketplace** during the parking period.

## Why parked, not deleted

Local fork being tuned: `~/radix-workspaces/rust-mastery/.claude/skills/radix/`

Tuning happens against a real corpus (Rust mastery, 53 sources, 9 iterations). Once the methodology stabilizes through the iterations, the local fork ports back here as a new minor version (≥ 0.4.0) and gets re-registered in `marketplace.json`.

## Last shipped version

`0.3.4` — frozen in this directory (renamed from `plugins/radix` to `plugins/_radix.parked-while-tuning` on 2026-05-06). The git history is preserved.

## To promote back

1. Copy mature methodology from workspace fork → here
2. Bump `plugin.json` version (≥ 0.4.0)
3. Restore the entry in `.claude-plugin/marketplace.json` (template below)
4. Rename directory back: `git mv _radix.parked-while-tuning radix`
5. Remove this `PARKED.md`

### Marketplace entry template

```json
{
  "name": "radix",
  "source": "./plugins/radix",
  "description": "...",
  "version": "0.4.0",
  "author": { "name": "Mox Labs", "email": "mox.rnd@gmail.com", "url": "https://github.com/mox-nexus" },
  "homepage": "https://github.com/mox-nexus/cix/tree/main/plugins/radix",
  "repository": "https://github.com/mox-nexus/cix",
  "license": "MIT",
  "keywords": ["code-mining", "tacit-knowledge", "expert-knowledge", "stewardship", "oscillations", "battle-scars", "type-signatures", "design-rationale", "git-archaeology", "rfc-archaeology", "session-continuity", "knowledge-corpus", "multi-session"],
  "category": "research"
}
```
