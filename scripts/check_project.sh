#!/usr/bin/env bash
# mehmet project health check
# Verifies the core project structure and documentation freshness.
# Used as CI test infrastructure (see .github/workflows/opencode.yml).
#
# Exit codes:
#   0  -> all required files present
#   1  -> a required file is missing

set -euo pipefail

REQUIRED_FILES=(
  "AGENTS.md"
  "CHANGELOG.md"
  "CONTRIBUTING.md"
  "LICENSE"
  "MATURITY.md"
  "PERSONALITY.md"
  "README.md"
  "SECURITY.md"
  "opencode.json"
  "pyproject.toml"
  "requirements.txt"
  "src/mehmet/__init__.py"
  "src/mehmet/maturity.py"
  "tests/test_maturity.py"
  ".github/workflows/opencode.yml"
  ".github/workflows/release.yml"
  "docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md"
  "docs/superpowers/plans/2026-07-04-mehmet-implementation.md"
)

fail=0
today="$(date +%Y-%m-%d)"

echo "==> Required files"
for f in "${REQUIRED_FILES[@]}"; do
  if [[ -f "$f" ]]; then
    echo "  [ok] $f"
  else
    echo "  [FAIL] $f missing"
    fail=1
  fi
done

echo "==> Freshness"
if grep -q -- "$today" CHANGELOG.md 2>/dev/null; then
  echo "  [ok] CHANGELOG.md entry for $today"
else
  echo "  [warn] CHANGELOG.md has no entry for $today"
fi

if grep -q -- "$today" PERSONALITY.md 2>/dev/null; then
  echo "  [ok] PERSONALITY.md escape log entry for $today"
else
  echo "  [warn] PERSONALITY.md escape log has no entry for $today"
fi

if [[ -f MATURITY.md ]] && grep -q "maturity.sh" MATURITY.md 2>/dev/null; then
  echo "  [ok] MATURITY.md references maturity script"
else
  echo "  [warn] MATURITY.md does not reference maturity script"
fi

echo "==> Markdown hygiene"
if grep -rnE "[[:blank:]]+$" --include="*.md" . 2>/dev/null | grep -v "^./.git/" >/dev/null; then
  echo "  [warn] trailing whitespace found in markdown files"
else
  echo "  [ok] no trailing whitespace in markdown files"
fi

echo "==> Scripts"
for s in scripts/check_project.sh scripts/maturity.sh; do
  if [[ -f "$s" ]]; then
    if [[ -x "$s" ]]; then
      echo "  [ok] $s executable"
    else
      echo "  [warn] $s not executable"
    fi
    if bash -n "$s" 2>/dev/null; then
      echo "  [ok] $s valid bash syntax"
    else
      echo "  [FAIL] $s has syntax errors"
      fail=1
    fi
  else
    echo "  [FAIL] $s missing"
    fail=1
  fi
done

echo "==> Python"
for m in src/mehmet/maturity.py tests/test_maturity.py; do
  if [[ -f "$m" ]]; then
    if python3 -m py_compile "$m" 2>/dev/null; then
      echo "  [ok] $m compiles"
    else
      echo "  [FAIL] $m has syntax errors"
      fail=1
    fi
  else
    echo "  [FAIL] $m missing"
    fail=1
  fi
done

echo
if [[ "$fail" -eq 1 ]]; then
  echo "RESULT: FAILURE — required files missing or invalid"
  exit 1
fi
echo "RESULT: OK — project structure intact"