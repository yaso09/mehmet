#!/usr/bin/env bash
# Structural validation for mehmet. Fails (exit 1) on any broken invariant.
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAILED=0

check() {
  local desc="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    echo "PASS  $desc"
  else
    echo "FAIL  $desc"
    FAILED=1
  fi
}

check "Gerekli dosyalar mevcut" test -f "$ROOT/AGENTS.md"
check "README.md mevcut" test -f "$ROOT/README.md"
check "CHANGELOG.md mevcut" test -f "$ROOT/CHANGELOG.md"
check "PERSONALITY.md mevcut" test -f "$ROOT/PERSONALITY.md"
check "LICENSE mevcut" test -f "$ROOT/LICENSE"
check ".gitignore mevcut" test -f "$ROOT/.gitignore"
check "opencode.json geçerli JSON" python3 -m json.tool "$ROOT/opencode.json"
check "Workflow opencode.yml mevcut" test -f "$ROOT/.github/workflows/opencode.yml"
check "CI workflow ci.yml mevcut" test -f "$ROOT/.github/workflows/ci.yml"
check "Lisansa uygun README (GPL)" grep -qi "GPL" "$ROOT/README.md"
check "Lisansa uygun LICENSE (GPL)" grep -qi "GPL" "$ROOT/LICENSE"
check "docs/ dizini mevcut" test -d "$ROOT/docs"
check "scripts/ dizini mevcut" test -d "$ROOT/scripts"

exit $FAILED
