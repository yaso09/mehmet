#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

CURRENT="$(cat VERSION)"
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"

case "${1:-patch}" in
  major) MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0 ;;
  minor) MINOR=$((MINOR + 1)); PATCH=0 ;;
  patch) PATCH=$((PATCH + 1)) ;;
  *)
    echo "Kullanım: scripts/bump-version.sh [major|minor|patch]" >&2
    exit 1
    ;;
esac

NEW="$MAJOR.$MINOR.$PATCH"
echo "$NEW" > VERSION
echo "$CURRENT -> $NEW"