#!/usr/bin/env bash
# install.sh — Install a skill from this repo into Claude Code
#
# Usage:
#   ./install.sh quiz-generator          # install a specific skill
#   ./install.sh                         # list available skills

set -e

SKILLS_DIR="$(cd "$(dirname "$0")/skills" && pwd)"
CLAUDE_SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"

# List available skills if no argument given
if [ -z "$1" ]; then
  echo "Available skills:"
  for skill in "$SKILLS_DIR"/*/; do
    name=$(basename "$skill")
    desc=$(grep -m1 'description:' "$skill/SKILL.md" 2>/dev/null | sed 's/description: *//' | tr -d '">' | cut -c1-80)
    printf "  %-20s %s\n" "$name" "$desc"
  done
  echo ""
  echo "Usage: $0 <skill-name>"
  exit 0
fi

SKILL_NAME="$1"
SKILL_SRC="$SKILLS_DIR/$SKILL_NAME"

if [ ! -d "$SKILL_SRC" ]; then
  echo "Error: skill '$SKILL_NAME' not found in $SKILLS_DIR"
  exit 1
fi

# Create destination and package as .skill zip
DEST="$CLAUDE_SKILLS_DIR"
mkdir -p "$DEST"

TMP_ZIP="/tmp/${SKILL_NAME}.skill"

cd "$SKILLS_DIR"
zip -r "$TMP_ZIP" "$SKILL_NAME/" -x "*.DS_Store" "**/__pycache__/*" > /dev/null

echo "Installing '$SKILL_NAME' into Claude Code..."
claude skill install "$TMP_ZIP"
rm -f "$TMP_ZIP"

echo ""
echo "✓ Skill '$SKILL_NAME' installed successfully."
echo "  You can now use it in Claude Code:"
echo ""
echo "  claude --file your-notes.md \"Generate study questions\""
echo ""
