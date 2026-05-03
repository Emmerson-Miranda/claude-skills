#!/usr/bin/env bash
# package.sh — Package all skills into .skill files in the releases/ folder
#
# Usage:
#   ./package.sh

set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$REPO_DIR/skills"
RELEASES_DIR="$REPO_DIR/releases"

mkdir -p "$RELEASES_DIR"

count=0

echo "Packaging skills into $RELEASES_DIR/"
echo ""

for skill_dir in "$SKILLS_DIR"/*/; do
  [ -d "$skill_dir" ] || continue
  name=$(basename "$skill_dir")
  out="$RELEASES_DIR/${name}.skill"

  cd "$SKILLS_DIR"
  zip -r "$out" "$name/" -x "*.DS_Store" "**/__pycache__/*" > /dev/null

  size=$(du -sh "$out" | cut -f1)
  echo "  ✓ ${name}.skill  (${size})"
  count=$((count + 1))
done

if [ "$count" -eq 0 ]; then
  echo "No skills found in $SKILLS_DIR"
  exit 0
fi

echo ""
echo "Done. $count skill(s) packaged."
