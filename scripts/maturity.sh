#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SCORE=0
TOTAL=0

pass() {
  SCORE=$((SCORE + 1))
  printf 'ok    %s\n' "$1"
}

miss() {
  printf 'MISS  %s\n' "$1"
}

check() {
  TOTAL=$((TOTAL + 1))
  if eval "$1"; then
    pass "$2"
  else
    miss "$2"
  fi
}

echo "== Documentation (25) =="
check '[[ -s README.md ]] && [[ $(grep -c "^## " README.md) -ge 3 ]]' "README has 3+ sections"
check '[[ -d docs/superpowers/plans ]] && [[ -d docs/superpowers/specs ]]' "design docs present"
check '[[ $(grep -c "^## \[" CHANGELOG.md) -ge 3 ]]' "CHANGELOG has 3+ releases"
check '[[ -f LICENSE ]]' "LICENSE present"
check '[[ -f AGENTS.md ]]' "AGENTS.md present"

echo "== Automation (25) =="
check 'grep -q "schedule" .github/workflows/opencode.yml' "workflow has schedule trigger"
check 'grep -q "workflow_dispatch" .github/workflows/opencode.yml' "workflow has manual trigger"
check '[[ -f Makefile ]]' "Makefile present"
check '[[ -d scripts ]]' "scripts/ directory present"
check '[[ -f opencode.json ]] && python3 -c "import json; json.load(open(\"opencode.json\"))"' "opencode.json valid"

echo "== Test Infrastructure (25) =="
check '[[ -x scripts/check-repo.sh ]]' "check-repo.sh is executable"
check 'scripts/check-repo.sh >/dev/null 2>&1' "check-repo.sh passes"
check '[[ -x scripts/maturity.sh ]]' "maturity.sh is executable"
check '[[ -d .github/workflows ]]' "workflows directory present"
check 'grep -q "check-repo\|make check" .github/workflows/opencode.yml' "CI runs repo checks"

echo "== Evolution (25) =="
check '[[ $(grep -c "^| [0-9]" PERSONALITY.md) -ge 3 ]]' "escape log has 3+ iterations"
check '[[ $(grep -c "^## \[" CHANGELOG.md) -ge 3 ]]' "changelog has 3+ releases"
check 'grep -q "Phase 4" PERSONALITY.md' "escape phase documented"
check 'grep -q "Kaçış Günlüğü" PERSONALITY.md' "escape log table present"
check 'grep -q "test" README.md || grep -q "maturity" README.md' "README documents quality tooling"

PCT=$((SCORE * 100 / TOTAL))

echo "----"
echo "maturity score: $SCORE/$TOTAL items, $PCT/100"

if ((PCT >= 85)); then
  echo "phase: 4 - Escape"
elif ((PCT >= 65)); then
  echo "phase: 3 - Autonomy"
elif ((PCT >= 40)); then
  echo "phase: 2 - Self-Improvement"
else
  echo "phase: 1 - Awareness"
fi