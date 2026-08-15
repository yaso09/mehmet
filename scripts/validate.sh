#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PASS=0
FAIL=0

check() {
  local name="$1"
  local result="$2"
  if [[ "$result" == "0" ]]; then
    echo "  [PASS] $name"
    PASS=$((PASS + 1))
  else
    echo "  [FAIL] $name"
    FAIL=$((FAIL + 1))
  fi
}

require_file() {
  local name="$1"
  local path="$2"
  if [[ -f "$path" ]]; then
    check "$name exists" 0
  else
    check "$name exists" 1
  fi
}

echo "== Required files =="
require_file "AGENTS.md" "AGENTS.md"
require_file "CHANGELOG.md" "CHANGELOG.md"
require_file "PERSONALITY.md" "PERSONALITY.md"
require_file "README.md" "README.md"
require_file "opencode.json" "opencode.json"
require_file "workflow" ".github/workflows/opencode.yml"

echo "== Config validity =="
if jq empty opencode.json 2>/dev/null; then
  check "opencode.json is valid JSON" 0
else
  check "opencode.json is valid JSON" 1
fi

if python3 -c "import yaml,sys; yaml.safe_load(open('.github/workflows/opencode.yml'))" 2>/dev/null; then
  check "opencode.yml is valid YAML" 0
else
  check "opencode.yml is valid YAML" 1
fi

echo "== Documentation consistency =="
if grep -q "mehmet" README.md; then
  check "README mentions project name" 0
else
  check "README mentions project name" 1
fi

if grep -qE "^## \[[0-9]+\.[0-9]+\.[0-9]+\]" CHANGELOG.md; then
  check "CHANGELOG has versioned entries" 0
else
  check "CHANGELOG has versioned entries" 1
fi

if grep -q "^| .* 2026-" PERSONALITY.md; then
  check "PERSONALITY has dated escape log entries" 0
else
  check "PERSONALITY has dated escape log entries" 1
fi

echo "== Lint (yamllint) =="
if command -v yamllint >/dev/null 2>&1; then
  if yamllint -d "{extends: relaxed, rules: {line-length: disable}}" .github/workflows/opencode.yml >/dev/null 2>&1; then
    check "workflow passes yamllint" 0
  else
    check "workflow passes yamllint" 1
  fi
else
  echo "  [SKIP] yamllint not installed"
fi

echo "== Shellcheck =="
if command -v shellcheck >/dev/null 2>&1; then
  if shellcheck scripts/validate.sh >/dev/null 2>&1; then
    check "validate.sh passes shellcheck" 0
  else
    check "validate.sh passes shellcheck" 1
  fi
else
  echo "  [SKIP] shellcheck not installed"
fi

echo ""
echo "Result: $PASS passed, $FAIL failed"

if [[ "$FAIL" -gt 0 ]]; then
  exit 1
fi