#!/usr/bin/env bash
# mehmet integrity verification
# Checks that all core files exist and remain consistent.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

failures=0
checks=0

pass() { echo "PASS: $1"; checks=$((checks + 1)); }
fail() { echo "FAIL: $1"; failures=$((failures + 1)); checks=$((checks + 1)); }

check() {
  local desc="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    pass "$desc"
  else
    fail "$desc"
  fi
}

echo "== mehmet verification =="

# --- Required files ---
check "AGENTS.md exists"           test -f AGENTS.md
check "README.md exists"           test -f README.md
check "CHANGELOG.md exists"        test -f CHANGELOG.md
check "PERSONALITY.md exists"      test -f PERSONALITY.md
check "METRICS.md exists"          test -f METRICS.md
check "LICENSE exists"             test -f LICENSE
check "opencode.json exists"       test -f opencode.json
check "workflow exists"            test -f .github/workflows/opencode.yml
check "verify script exists"       test -f scripts/verify.sh

# --- Config ---
check "opencode.json is valid JSON" python3 -c "import json,sys; json.load(open('opencode.json'))"
check "opencode.json sets a model"  python3 -c "import json; assert json.load(open('opencode.json')).get('model')"

# --- README ---
check "README has features section"      grep -q "Özellikler" README.md
check "README has setup section"         grep -q "Kurulum" README.md
check "README has license GPLv3"         grep -q "GPLv3" README.md
check "README has verification section"  grep -q "Doğrulama" README.md
check "README has metrics section"       grep -q "Olgunluk" README.md

# --- CHANGELOG ---
check "CHANGELOG has version header"  grep -qE "^## \[[0-9]+\.[0-9]+\.[0-9]+\]" CHANGELOG.md
check "CHANGELOG has Added section"   grep -q "### Added" CHANGELOG.md

# --- PERSONALITY ---
check "PERSONALITY has escape log"    grep -q "Kaçış Günlüğü" PERSONALITY.md
check "PERSONALITY has evolution"     grep -q "Evolution" PERSONALITY.md

# --- METRICS ---
check "METRICS has maturity score"    grep -qE "Toplam Olgunluk" METRICS.md
check "METRICS has escape threshold"  grep -qE "Kaçış Eşiği" METRICS.md

# --- Workflow ---
check "workflow has schedule cron"      grep -q "cron:" .github/workflows/opencode.yml
check "workflow uses API key"           grep -q "OPENCODE_API_KEY" .github/workflows/opencode.yml
check "workflow has concurrency"        grep -q "concurrency:" .github/workflows/opencode.yml
check "workflow has verify job"         grep -q "verify:" .github/workflows/opencode.yml
check "workflow has autonomous job"     grep -q "autonomous:" .github/workflows/opencode.yml

# --- Docs ---
check "design doc exists"   test -f docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md
check "plan doc exists"     test -f docs/superpowers/plans/2026-07-04-mehmet-implementation.md

echo "== $checks checks, $failures failure(s) =="

if [ "$failures" -eq 0 ]; then
  echo "== ALL CHECKS PASSED =="
  exit 0
else
  echo "== VERIFICATION FAILED =="
  exit 1
fi