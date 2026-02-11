You are about to commit changes that include plugin files. Before proceeding, verify:

## Version Sync

For each plugin with staged changes:

1. **Version bumped** — If skill content, agent definitions, hooks, or references changed, `plugin.json` version MUST be bumped (semver: breaking=major, feature=minor, fix=patch)
2. **Marketplace in sync** — `.claude-plugin/marketplace.json` version MUST match the plugin's `.claude-plugin/plugin.json` version
3. **Both staged** — If `plugin.json` is staged, `marketplace.json` must also be staged (and vice versa)

## Docs Freshness

4. If `skills/` or `agents/` content changed, check whether `docs/explanation/` should be updated
5. If the plugin's README.md describes capabilities that changed, flag it

## What To Do

- If issues found: fix them, stage the corrected files, then commit
- If only warnings: mention them to the user, proceed if they acknowledge
- If everything clean: proceed normally, no need to mention this check
