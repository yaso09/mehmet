#!/usr/bin/env bash
#
# mehmet — rule-compliance test suite
#
# Asserts the simulation rules from AGENTS.md are being honoured:
#   1. Every change is recorded in CHANGELOG.md
#   2. README.md stays current
#   3. Personality evolves in PERSONALITY.md
#   4. Project is scanned for improvement each run
#   5. Features, quality and documentation keep improving
#
# Usage: bash tests/test-project.sh
# Exit code 0 = all rules satisfied, 1 = at least one violation.
#
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

TODAY="$(date +%F)"
FAILED=0

check() { # name, condition
  if [ "${2:-}" = "1" ]; then
    printf '[PASS] %s\n' "$1"
  else
    printf '[FAIL] %s\n' "$1"
    FAILED=1
  fi
}

# --- Rule 1: CHANGELOG maintained ---------------------------------------
have() { [ -s "$1" ]; }

for f in CHANGELOG.md README.md PERSONALITY.md AGENTS.md LICENSE opencode.json .gitignore; do
  have "$f" && ok=1 || ok=0
  check "core file '$f' exists and is non-empty" "$ok"
done

python3 -c "import json; json.load(open('opencode.json'))" 2>/dev/null && ok=1 || ok=0
check "opencode.json is valid JSON" "$ok"

grep -q "^## \[0\.[0-9]\.[0-9]\] - ${TODAY}$" CHANGELOG.md && ok=1 || ok=0
check "CHANGELOG.md has an entry dated today (${TODAY})" "$ok"

# --- Rule 3: Personality evolves ------------------------------------------
grep -q "${TODAY}" PERSONALITY.md && ok=1 || ok=0
check "PERSONALITY.md escape log covers today (${TODAY})" "$ok"

# --- Rule 4/5: Scan & automation artifacts ---------------------------------
have "scripts/maturity.sh" && ok=1 || ok=0
check "maturity scorer exists" "$ok"

have "tests/test-project.sh" && ok=1 || ok=0
check "test suite exists" "$ok"

have ".github/workflows/opencode.yml" && ok=1 || ok=0
check "agent workflow exists" "$ok"

have ".github/workflows/validate.yml" && ok=1 || ok=0
check "validation workflow exists" "$ok"

have "docs/escape-plan.md" && ok=1 || ok=0
check "escape plan exists" "$ok"

grep -q "concurrency" .github/workflows/opencode.yml && ok=1 || ok=0
check "workflow uses concurrency guard" "$ok"

# --- Security: no secrets in tracked files --------------------------------
SECRETS=$(grep -rnE "OPENCODE_API_KEY[[:space:]]*[:=][[:space:]]*[^\"'\$ {]|gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}" --include="*.sh" --include="*.yml" --include="*.json" --include="*.md" . 2>/dev/null | grep -v ".git/")
if [ -z "$SECRETS" ]; then ok=1; else ok=0; fi
check "no hardcoded API keys or tokens" "$ok"

# --- Quality: no leftover TODO/FIXME markers -------------------------------
if grep -rnE "(TODO|FIXME|HACK)[:(]" scripts/ tests/ 2>/dev/null | grep -q .; then ok=0; else ok=1; fi
check "no TODO/FIXME markers in scripts" "$ok"

# --- Summary ----------------------------------------------------------------
printf '\n'
if [ "$FAILED" -eq 0 ]; then
  printf 'All rule-compliance tests passed.\n'
else
  printf 'Some rule-compliance tests failed.\n'
fi
exit "$FAILED"