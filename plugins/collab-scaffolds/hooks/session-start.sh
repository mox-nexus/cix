#!/bin/sh
# Outputs plugin triggers from cix marketplace
# POSIX-compliant

MARKETPLACES_FILE="$HOME/.claude/plugins/known_marketplaces.json"

# Get install location if marketplace exists
if [ -f "$MARKETPLACES_FILE" ]; then
  INSTALL_LOC=$(grep -A5 '"cix"' "$MARKETPLACES_FILE" 2>/dev/null | grep 'installLocation' | sed 's/.*: *"\([^"]*\)".*/\1/')
fi

# Always output collab-scaffolds instruction
echo "## cix"
echo ""
echo "**Load now:** \`$INSTALL_LOC/plugins/collab-scaffolds/SKILL.md\`"

# If we have the marketplace, show the trigger table
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
