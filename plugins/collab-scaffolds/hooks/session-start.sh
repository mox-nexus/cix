#!/bin/sh
# SessionStart: Load collab-scaffolds skills + discover other cix plugins
# Uses CLAUDE_PLUGIN_ROOT for own skills (reliable), marketplace lookup for siblings

# Collab skills — always available via CLAUDE_PLUGIN_ROOT
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-.}"

echo "## cix"
echo ""
echo "**Load now:** \`${PLUGIN_ROOT}/skills/crafting/SKILL.md\`"
echo "**Collaboration:** \`${PLUGIN_ROOT}/skills/collaborating/SKILL.md\`"
echo "**Problem solving:** \`${PLUGIN_ROOT}/skills/problem-solving/SKILL.md\`"

# Discover sibling plugins via marketplace (best-effort)
MARKETPLACES_FILE="$HOME/.claude/plugins/known_marketplaces.json"

if [ -f "$MARKETPLACES_FILE" ]; then
  INSTALL_LOC=$(grep -A5 '"cix"' "$MARKETPLACES_FILE" 2>/dev/null | grep 'installLocation' | sed 's/.*: *"\([^"]*\)".*/\1/')
fi

if [ -n "$INSTALL_LOC" ] && [ -f "$INSTALL_LOC/.claude-plugin/marketplace.json" ]; then
  echo ""
  echo "**Other plugins** (load when relevant):"
  echo ""

  awk -F'"' -v loc="$INSTALL_LOC" '
    /"name":/ { name = $4 }
    /"description":/ && /Use when:/ {
      desc = $4
      sub(/.*Use when: /, "", desc)
      sub(/\..*/, "", desc)
      if (name != "collab-scaffolds" && name != "") {
        print "- **" name "** → " desc " → `" loc "/plugins/" name "/SKILL.md`"
      }
    }
  ' "$INSTALL_LOC/.claude-plugin/marketplace.json"
fi
