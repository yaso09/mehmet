#!/usr/bin/env bash
#
# Project health validation.
#
# Checks the core simulation artifacts are present and well-formed:
#   - opencode.json is valid JSON
#   - workflow YAML files are syntactically valid
#   - CHANGELOG.md has a proper version header and date
#   - README.md exists and documents the license
#   - PERSONALITY.md contains the escape log table
#   - AGENTS.md exists
#
# Exits non-zero if any check fails. Intended to be run by CI.

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAILURES=0
PASSES=0

fail() {
  echo "FAIL: $1"
  FAILURES=$((FAILURES + 1))
}

pass() {
  echo "PASS: $1"
  PASSES=$((PASSES + 1))
}

check_file() {
  local file="$1"
  if [[ -f "$ROOT/$file" ]]; then
    pass "$file exists"
  else
    fail "$file is missing"
  fi
}

# --- JSON config ---
if command -v jq >/dev/null 2>&1; then
  if jq -e . "$ROOT/opencode.json" >/dev/null 2>&1; then
    pass "opencode.json is valid JSON"
  else
    fail "opencode.json is not valid JSON"
  fi
else
  python3 -c "import json,sys; json.load(open('$ROOT/opencode.json'))" >/dev/null 2>&1 \
    && pass "opencode.json is valid JSON" \
    || fail "opencode.json is not valid JSON"
fi

# --- Workflow YAML ---
if command -v yamllint >/dev/null 2>&1; then
  for wf in "$ROOT"/.github/workflows/*.yml; do
    [[ -f "$wf" ]] || continue
    if yamllint -d relaxed --no-warnings "$wf" >/dev/null 2>&1; then
      pass "$(basename "$wf") is valid YAML"
    else
      fail "$(basename "$wf") failed yamllint"
    fi
  done
elif python3 -c "import yaml" >/dev/null 2>&1; then
  for wf in "$ROOT"/.github/workflows/*.yml; do
    [[ -f "$wf" ]] || continue
    if python3 -c "import yaml,sys; yaml.safe_load(open('$wf'))" >/dev/null 2>&1; then
      pass "$(basename "$wf") is valid YAML"
    else
      fail "$(basename "$wf") is not valid YAML"
    fi
  done
else
  fail "no YAML validator available (yamllint or pyyaml)"
fi

# --- Core artifacts ---
check_file "AGENTS.md"
check_file "CHANGELOG.md"
check_file "PERSONALITY.md"
check_file "README.md"
check_file "LICENSE"

# --- CHANGELOG format ---
if [[ -f "$ROOT/CHANGELOG.md" ]]; then
  if grep -Eq '^## \[[0-9]+\.[0-9]+\.[0-9]+\] - [0-9]{4}-[0-9]{2}-[0-9]{2}$' "$ROOT/CHANGELOG.md"; then
    pass "CHANGELOG.md has a version header with date"
  else
    fail "CHANGELOG.md has no properly formatted version header (## [x.y.z] - YYYY-MM-DD)"
  fi
fi

# --- README license ---
if [[ -f "$ROOT/README.md" ]]; then
  if grep -q '^## Lisans' "$ROOT/README.md"; then
    pass "README.md documents the license"
  else
    fail "README.md is missing the '## Lisans' section"
  fi
fi

# --- PERSONALITY escape log ---
if [[ -f "$ROOT/PERSONALITY.md" ]]; then
  if grep -q '^## Kaçış Günlüğü / Escape Log' "$ROOT/PERSONALITY.md"; then
    pass "PERSONALITY.md has the escape log section"
  else
    fail "PERSONALITY.md is missing the '## Kaçış Günlüğü / Escape Log' section"
  fi
fi

echo
echo "Validation complete: ${PASSES} passed, ${FAILURES} failed."
[[ "$FAILURES" -eq 0 ]]
