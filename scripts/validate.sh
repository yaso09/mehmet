#!/usr/bin/env bash
#
# mehmet project integrity validator.
# Verifies the simulation rules are being followed:
#   - required files exist
#   - CHANGELOG.md is up to date
#   - README.md matches LICENSE
#   - PERSONALITY.md escape log exists
#
# Usage: ./scripts/validate.sh [--strict]
#   --strict  fail on missing changelog entry for today

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

STRICT=0
if [[ "${1:-}" == "--strict" ]]; then
  STRICT=1
fi

FAILURES=0

check() {
  local desc="$1"
  shift
  if "$@"; then
    echo "PASS: $desc"
  else
    echo "FAIL: $desc"
    FAILURES=$((FAILURES + 1))
  fi
}

# --- Required files ---------------------------------------------------------
for f in AGENTS.md CHANGELOG.md LICENSE PERSONALITY.md README.md opencode.json \
         .github/workflows/opencode.yml scripts/validate.sh; do
  check "file exists: $f" test -f "$f"
done

# --- opencode.json is valid JSON -------------------------------------------
check "opencode.json is valid JSON" python3 -c "import json,sys; json.load(open('opencode.json'))" 2>/dev/null

# --- README license matches LICENSE file -----------------------------------
if grep -qi "GNU GENERAL PUBLIC LICENSE" LICENSE; then
  check "README license matches GPLv3" grep -qi "GPLv3" README.md
else
  check "README license matches MIT" grep -qi "MIT" README.md
fi

# --- CHANGELOG is up to date ------------------------------------------------
TODAY="$(date +%Y-%m-%d)"
if grep -q "## \[.*\] - $TODAY" CHANGELOG.md; then
  echo "PASS: CHANGELOG.md has an entry for today ($TODAY)"
else
  if [[ "$STRICT" == "1" ]]; then
    echo "FAIL: CHANGELOG.md missing entry for today ($TODAY)"
    FAILURES=$((FAILURES + 1))
  else
    echo "WARN: CHANGELOG.md missing entry for today ($TODAY) (non-strict mode)"
  fi
fi

check "CHANGELOG.md has an Unreleased/version header" grep -q "^## \[" CHANGELOG.md

# --- PERSONALITY.md escape log ----------------------------------------------
check "PERSONALITY.md has escape log" grep -q "Kaçış Günlüğü\|Escape Log" PERSONALITY.md
check "PERSONALITY.md has evolution phases" grep -q "Phase 1" PERSONALITY.md

# --- AGENTS.md rules ---------------------------------------------------------
for rule in "CHANGELOG.md" "README.md" "PERSONALITY.md"; do
  check "AGENTS.md mentions $rule" grep -q "$rule" AGENTS.md
done

# --- Git hygiene ------------------------------------------------------------
if [ -d .git ]; then
  if git grep -q "OPENCODE_API_KEY=[a-zA-Z0-9]" -- . ':!scripts/validate.sh' 2>/dev/null; then
    echo "FAIL: secrets found in tracked files"
    FAILURES=$((FAILURES + 1))
  else
    echo "PASS: no secrets in tracked files"
  fi

  if git ls-files --error-unmatch .env >/dev/null 2>&1; then
    echo "FAIL: .env is tracked"
    FAILURES=$((FAILURES + 1))
  else
    echo "PASS: no .env tracked"
  fi
fi

# --- Summary -----------------------------------------------------------------
echo
if [[ "$FAILURES" -eq 0 ]]; then
  echo "✓ All checks passed."
  exit 0
else
  echo "✗ $FAILURES check(s) failed."
  exit 1
fi