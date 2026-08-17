#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

THRESHOLD="${1:-80}"
failures=0

report() {
  if [ "$2" = "ok" ]; then
    printf '  [OK]   %s\n' "$1"
  else
    printf '  [FAIL] %s\n' "$1"
    failures=$((failures + 1))
  fi
}

echo "== Project Health Check =="

# --- Required files ---
for f in AGENTS.md CHANGELOG.md LICENSE PERSONALITY.md README.md opencode.json; do
  if [ -f "$f" ]; then
    report "$f present" ok
  else
    report "$f present" fail
  fi
done

# --- opencode.json validity ---
if python3 -m json.tool opencode.json >/dev/null 2>&1; then
  report "opencode.json is valid JSON" ok
else
  report "opencode.json is valid JSON" fail
fi

# --- CHANGELOG has releases ---
if grep -q "## \[" CHANGELOG.md; then
  report "CHANGELOG has releases" ok
else
  report "CHANGELOG has releases" fail
fi

# --- README license consistency ---
if grep -qi "GPLv3" README.md; then
  report "README license consistent" ok
else
  report "README license consistent" fail
fi

# --- Escape log entries exist ---
if grep -q "^| [0-9]" PERSONALITY.md; then
  report "escape log has entries" ok
else
  report "escape log has entries" fail
fi

# --- Workflow files exist ---
for f in .github/workflows/opencode.yml .github/workflows/ci.yml; do
  if [ -f "$f" ]; then
    report "$f present" ok
  else
    report "$f present" fail
  fi
done

# --- Maturity gate ---
echo ""
echo "== Maturity Score =="
maturity_output=$(bash scripts/maturity-score.sh)
printf '%s\n' "$maturity_output"
score=$(printf '%s\n' "$maturity_output" | grep "TOTAL MATURITY SCORE" | grep -o '[0-9]*' | head -n1)
score=${score:-0}

echo ""
if [ "$score" -ge "$THRESHOLD" ]; then
  report "maturity score >= $THRESHOLD ($score)" ok
else
  report "maturity score >= $THRESHOLD ($score)" fail
fi

echo ""
if [ "$failures" -eq 0 ]; then
  echo "RESULT: All health checks passed."
else
  echo "RESULT: $failures health check(s) failed."
  exit 1
fi
