#!/usr/bin/env bash
#
# Project integrity validation for mehmet.
# Verifies required files, config syntax and documentation consistency.
# Used by CI and by the autonomous agent after each iteration.

set -euo pipefail

FAILURES=0

say() { printf '%s\n' "$*"; }
pass() { say "  [OK] $*"; }
fail() { say "  [FAIL] $*"; FAILURES=$((FAILURES + 1)); }

say "==> Checking required files"
REQUIRED_FILES=(
  "AGENTS.md"
  "CHANGELOG.md"
  "LICENSE"
  "PERSONALITY.md"
  "README.md"
  "opencode.json"
  ".github/workflows/opencode.yml"
)
for f in "${REQUIRED_FILES[@]}"; do
  if [[ -f "$f" ]]; then
    pass "exists: $f"
  else
    fail "missing: $f"
  fi
done

say "==> Validating opencode.json"
if command -v python3 >/dev/null 2>&1; then
  if python3 -c 'import json,sys; json.load(open("opencode.json"))' 2>/dev/null; then
    pass "opencode.json is valid JSON"
  else
    fail "opencode.json is not valid JSON"
  fi
else
  say "  [SKIP] python3 not available, skipping JSON validation"
fi

say "==> Validating workflow YAML files"
YAML_AVAILABLE=0
if command -v python3 >/dev/null 2>&1 && python3 -c 'import yaml' 2>/dev/null; then
  YAML_AVAILABLE=1
fi
for f in .github/workflows/*.yml; do
  if [[ "$YAML_AVAILABLE" == "1" ]]; then
    if python3 -c 'import yaml,sys; yaml.safe_load(open(sys.argv[1]))' "$f" 2>/dev/null; then
      pass "$f is valid YAML"
    else
      fail "$f is not valid YAML"
    fi
  else
    if grep -q '^[A-Za-z_]*:' "$f"; then
      pass "$f looks like YAML (basic check)"
    else
      fail "$f does not look like YAML"
    fi
  fi
done

say "==> Checking documentation consistency"
if grep -q '^## .*\[[0-9]\+\.[0-9]\+\.[0-9]\+\]' CHANGELOG.md; then
  pass "CHANGELOG.md has a version section"
else
  fail "CHANGELOG.md has no version section"
fi

if grep -q '^# ' README.md; then
  pass "README.md has a top-level heading"
else
  fail "README.md has no top-level heading"
fi

if grep -q 'Kaçış Günlüğü\|Escape Log' PERSONALITY.md; then
  pass "PERSONALITY.md has an escape log"
else
  fail "PERSONALITY.md has no escape log"
fi

if grep -q 'OPENCODE_API_KEY' .github/workflows/opencode.yml; then
  pass "workflow references OPENCODE_API_KEY secret"
else
  fail "workflow does not reference OPENCODE_API_KEY secret"
fi

say "==> Checking for stray secrets"
if grep -rn -E '(ghp_|sk-[A-Za-z0-9]{20,}|BEGIN (RSA|OPENSSH) PRIVATE KEY)' --include='*.md' --include='*.json' --include='*.yml' . 2>/dev/null; then
  fail "possible secret material found (see above)"
else
  pass "no obvious secret material"
fi

say
if [[ "$FAILURES" -gt 0 ]]; then
  say "Validation FAILED: $FAILURES problem(s)."
  exit 1
fi

say "Validation passed."