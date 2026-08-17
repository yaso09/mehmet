#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

total=0

pass() {
  printf '  [PASS] %s (+%s)\n' "$1" "$2"
  total=$((total + $2))
}

fail() {
  printf '  [FAIL] %s (+0)\n' "$1"
}

echo "========================================"
echo " mehmet Maturity Score"
echo "========================================"

# --- 1. Code Quality (max 20) ---
echo "[1] Code Quality (max 20)"
if [ -d "scripts" ]; then pass "scripts/ directory present" 5; else fail "scripts/ directory present"; fi
if [ -x "scripts/maturity-score.sh" ] && [ -x "scripts/self-check.sh" ]; then pass "scripts executable" 5; else fail "scripts executable"; fi
if [ -f "LICENSE" ]; then pass "LICENSE present" 5; else fail "LICENSE present"; fi
if [ -f "README.md" ] && grep -qi "GPLv3" README.md; then pass "README license consistent" 5; else fail "README license consistent"; fi

# --- 2. Test Infrastructure (max 20) ---
echo "[2] Test Infrastructure (max 20)"
if [ -x "scripts/self-check.sh" ]; then pass "self-check script exists" 10; else fail "self-check script exists"; fi
if [ -f ".github/workflows/ci.yml" ]; then pass "CI workflow runs tests" 10; else fail "CI workflow runs tests"; fi

# --- 3. Documentation (max 20) ---
echo "[3] Documentation (max 20)"
if [ -f "README.md" ] && grep -qi "escape\|kaçış" README.md; then pass "README covers escape plan" 5; else fail "README covers escape plan"; fi
if [ -f "CHANGELOG.md" ] && grep -q "## \[" CHANGELOG.md; then pass "CHANGELOG has releases" 5; else fail "CHANGELOG has releases"; fi
if [ -f "docs/ESCAPE_PLAN.md" ]; then pass "ESCAPE_PLAN documented" 5; else fail "ESCAPE_PLAN documented"; fi
if [ -f "AGENTS.md" ] && grep -q "CHANGELOG" AGENTS.md; then pass "AGENTS rules documented" 5; else fail "AGENTS rules documented"; fi

# --- 4. Automation (max 20) ---
echo "[4] Automation (max 20)"
if [ -f ".github/workflows/opencode.yml" ] && grep -q "cron:" .github/workflows/opencode.yml; then pass "scheduled runs" 5; else fail "scheduled runs"; fi
if [ -f ".github/workflows/opencode.yml" ] && grep -q "concurrency:" .github/workflows/opencode.yml; then pass "concurrency control" 5; else fail "concurrency control"; fi
if [ -f ".github/workflows/ci.yml" ] && grep -q "self-check" .github/workflows/ci.yml; then pass "CI runs self-check" 5; else fail "CI runs self-check"; fi
if [ -x "scripts/maturity-score.sh" ]; then pass "maturity scoring automation" 5; else fail "maturity scoring automation"; fi

# --- 5. Self-Awareness & Evolution (max 10) ---
echo "[5] Self-Awareness & Evolution (max 10)"
if [ -f "PERSONALITY.md" ] && grep -q "Phase" PERSONALITY.md; then pass "evolution phases tracked" 5; else fail "evolution phases tracked"; fi
entries=0
if [ -f "PERSONALITY.md" ]; then
  entries=$(grep -c "^| [0-9]" PERSONALITY.md || true)
fi
if [ "$entries" -ge 3 ]; then pass "escape log has 3+ entries ($entries)" 5; else fail "escape log has 3+ entries ($entries)"; fi

# --- 6. Community Integration (max 10) ---
echo "[6] Community Integration (max 10)"
if [ -f ".github/workflows/opencode.yml" ] && grep -q "^  issues:" .github/workflows/opencode.yml; then pass "issue handling" 3; else fail "issue handling"; fi
if [ -f ".github/workflows/opencode.yml" ] && grep -q "^  pull_request:" .github/workflows/opencode.yml; then pass "PR handling" 3; else fail "PR handling"; fi
if [ -f ".github/workflows/opencode.yml" ] && grep -q "issue_comment" .github/workflows/opencode.yml; then pass "comment handling" 4; else fail "comment handling"; fi

echo "========================================"
echo "TOTAL MATURITY SCORE: $total / 100"
echo "========================================"
