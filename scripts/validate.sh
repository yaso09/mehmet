#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

FAILURES=0

fail() {
  echo "FAIL: $1"
  FAILURES=$((FAILURES + 1))
}

pass() {
  echo "PASS: $1"
}

check_file() {
  if [[ -f "$1" ]]; then
    pass "file exists: $1"
  else
    fail "missing file: $1"
  fi
}

REQUIRED_FILES=(
  "AGENTS.md"
  "CHANGELOG.md"
  "LICENSE"
  "PERSONALITY.md"
  "README.md"
  "opencode.json"
  ".gitignore"
  ".github/workflows/opencode.yml"
)

for f in "${REQUIRED_FILES[@]}"; do
  check_file "$f"
done

if jq -e . opencode.json >/dev/null 2>&1; then
  pass "opencode.json is valid JSON"
  MODEL="$(jq -r '.model' opencode.json)"
  if [[ -n "$MODEL" && "$MODEL" != "null" ]]; then
    pass "opencode.json defines model: $MODEL"
  else
    fail "opencode.json missing model"
  fi
else
  fail "opencode.json is not valid JSON"
fi

if python3 -c "import yaml,sys; yaml.safe_load(open('.github/workflows/opencode.yml')); yaml.safe_load(open('.github/workflows/ci.yml'))" >/dev/null 2>&1; then
  pass "workflow YAML files parse"
else
  fail "workflow YAML files do not parse"
fi

if grep -q "^## \[[0-9]" CHANGELOG.md; then
  pass "CHANGELOG.md has version entries"
else
  fail "CHANGELOG.md has no version entries"
fi

if grep -rEn "sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}" --exclude-dir=.git . >/dev/null 2>&1; then
  fail "possible secret literal committed"
else
  pass "no secret literals committed"
fi

if grep -q "OPENCODE_API_KEY" .github/workflows/opencode.yml; then
  pass "workflow references OPENCODE_API_KEY secret placeholder only"
else
  fail "workflow does not reference OPENCODE_API_KEY"
fi

BANNER="$(head -1 README.md)"
if [[ "$BANNER" == "# mehmet" ]]; then
  pass "README.md title is correct"
else
  fail "README.md title incorrect"
fi

echo ""
if [[ "$FAILURES" -gt 0 ]]; then
  echo "Validation failed: $FAILURES error(s)"
  exit 1
fi
echo "All checks passed."