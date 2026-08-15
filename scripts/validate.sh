#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
failures=0

pass() {
  echo "PASS: $1"
}

fail() {
  echo "FAIL: $1"
  failures=$((failures + 1))
}

check_file() {
  local desc="$1"
  local path="$2"
  if [ -f "$ROOT/$path" ]; then
    pass "$desc ($path)"
  else
    fail "$desc ($path)"
  fi
}

check_file "AGENTS.md exists" "AGENTS.md"
check_file "CHANGELOG.md exists" "CHANGELOG.md"
check_file "PERSONALITY.md exists" "PERSONALITY.md"
check_file "README.md exists" "README.md"
check_file "opencode.json exists" "opencode.json"
check_file "Main workflow exists" ".github/workflows/opencode.yml"
check_file "CI workflow exists" ".github/workflows/ci.yml"

if command -v python3 >/dev/null 2>&1; then
  if python3 -c "import json,sys; json.load(open('$ROOT/opencode.json'))" 2>/dev/null; then
    pass "opencode.json is valid JSON"
  else
    fail "opencode.json is valid JSON"
  fi
elif command -v node >/dev/null 2>&1; then
  if node -e "require('$ROOT/opencode.json')" 2>/dev/null; then
    pass "opencode.json is valid JSON"
  else
    fail "opencode.json is valid JSON"
  fi
else
  fail "no JSON validator available (python3 or node required)"
fi

today="$(date +%Y-%m-%d)"
if grep -q "## \[[^]]*\] - $today" "$ROOT/CHANGELOG.md" 2>/dev/null; then
  pass "CHANGELOG.md has an entry for $today"
else
  fail "CHANGELOG.md missing entry for $today"
fi

if grep -q "| [0-9]* *| *$today " "$ROOT/PERSONALITY.md" 2>/dev/null; then
  pass "PERSONALITY.md escape log has an entry for $today"
else
  fail "PERSONALITY.md escape log missing entry for $today"
fi

echo ""
if [ "$failures" -gt 0 ]; then
  echo "$failures check(s) FAILED"
  exit 1
fi
echo "All checks passed"