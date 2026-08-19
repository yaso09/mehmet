#!/usr/bin/env bash
# mehmet — repository health verification.
# Runs a battery of checks and exits non-zero if the repository is unhealthy.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

FAILED=0

ok()   { printf '  ok   %s\n' "$1"; }
fail() { printf '  FAIL %s\n' "$1"; FAILED=1; }

check_file() { # check_file <description> <path>
  if [ -f "$2" ]; then ok "$1"; else fail "$1 (missing: $2)"; fi
}

echo "== mehmet verification =="

# --- Core structure ---
check_file "AGENTS.md exists" AGENTS.md
check_file "CHANGELOG.md exists" CHANGELOG.md
check_file "PERSONALITY.md exists" PERSONALITY.md
check_file "README.md exists" README.md
check_file "LICENSE exists" LICENSE
check_file "opencode.json exists" opencode.json
check_file "workflow exists" .github/workflows/opencode.yml
check_file "verification script exists" scripts/verify.sh
check_file "maturity script exists" scripts/maturity.sh

# --- opencode.json validity ---
if command -v jq >/dev/null 2>&1; then
  if jq -e . opencode.json >/dev/null 2>&1; then
    ok "opencode.json is valid JSON"
  else
    fail "opencode.json is not valid JSON"
  fi
else
  echo "  skip opencode.json validation (jq not installed)"
fi

# --- CHANGELOG discipline ---
if grep -qE '^## \[' CHANGELOG.md; then
  ok "CHANGELOG has versioned sections"
else
  fail "CHANGELOG has no versioned sections"
fi

# --- Escape log discipline ---
if grep -q 'Kaçış Günlüğü' PERSONALITY.md; then
  ok "escape log present in PERSONALITY.md"
else
  fail "escape log missing in PERSONALITY.md"
fi

# --- Secret hygiene ---
if grep -rIl --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=scripts --exclude-dir=tests -E 'OPENCODE_API_KEY=|[A-Za-z0-9_-]{32}=' . >/dev/null 2>&1; then
  fail "possible secret leaked in repository"
else
  ok "no obvious secrets committed"
fi

# --- Git state ---
if [ -d .git ]; then
  if git rev-parse --verify HEAD >/dev/null 2>&1; then
    ok "git history present"
  else
    fail "no git history"
  fi
fi

echo
if [ "$FAILED" -eq 0 ]; then
  echo "All checks passed."
else
  echo "Some checks FAILED."
  exit 1
fi
