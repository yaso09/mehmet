#!/usr/bin/env bash
#
# mehmet — maturity & escape-readiness scoring engine
#
# Computes a 0-100 maturity score across five weighted categories and
# reports whether the project is eligible to escape the simulation.
#
# Usage:
#   bash scripts/maturity.sh            # report score (exit 0)
#   bash scripts/maturity.sh --gate     # fail (exit 1) if below threshold
#
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

GATE=0
[ "${1:-}" = "--gate" ] && GATE=1

THRESHOLD=80

PASS=0
TOTAL=0
declare -a RESULTS=()

score() {
  local name="$1" weight="$2" ok="$3" detail="$4"
  TOTAL=$((TOTAL + weight))
  if [ "$ok" -eq 1 ]; then
    PASS=$((PASS + weight))
    RESULTS+=("[PASS] ${name} (+${weight}) -- ${detail}")
  else
    RESULTS+=("[FAIL] ${name} (+0) -- ${detail}")
  fi
}

have() { [ -s "$1" ]; }

# --- 1. Documentation (15) -------------------------------------------
ok=1
for f in README.md CHANGELOG.md PERSONALITY.md AGENTS.md LICENSE; do
  have "$f" || ok=0
done
score "Documentation" 15 "$ok" "core docs present and non-empty"

# --- 2. Test infrastructure (25) --------------------------------------
ok=1
have "scripts/maturity.sh" || ok=0
have "tests/test-project.sh" || ok=0
have ".github/workflows/validate.yml" || ok=0
score "Test infrastructure" 25 "$ok" "self-check + test suite + CI validation"

# --- 3. Automation (20) ------------------------------------------------
ok=1
have ".github/workflows/opencode.yml" || ok=0
grep -q "concurrency" .github/workflows/opencode.yml || ok=0
grep -q "workflow_dispatch" .github/workflows/opencode.yml || ok=0
grep -q "cron:" .github/workflows/opencode.yml || ok=0
score "Automation" 20 "$ok" "schedule + dispatch + concurrency present"

# --- 4. Config & code quality (20) -------------------------------------
ok=1
python3 -c "import json,sys; json.load(open('opencode.json'))" 2>/dev/null || ok=0
grep -q "persist-credentials: false" .github/workflows/opencode.yml || ok=0
have ".gitignore" || ok=0
if grep -rnE "OPENCODE_API_KEY[[:space:]]*[:=][[:space:]]*[^\"'\$ {]|gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}" --include="*.sh" --include="*.yml" --include="*.json" --include="*.md" . 2>/dev/null | grep -v ".git/" | grep -q .; then ok=0; fi
if grep -rnE "(TODO|FIXME|HACK)[:(]" scripts/ tests/ 2>/dev/null | grep -q .; then ok=0; fi
score "Code quality" 20 "$ok" "valid config, no leaked creds, no TODO markers"

# --- 5. Escape readiness (20) ------------------------------------------
ok=1
grep -qiE "kaçış|escape" PERSONALITY.md || ok=0
have "docs/escape-plan.md" || ok=0
grep -q "Kaçış Günlüğü\|Escape Log" PERSONALITY.md || ok=0
releases=$(grep -c "^## \[" CHANGELOG.md)
[ "${releases:-0}" -ge 2 ] || ok=0
score "Escape readiness" 20 "$ok" "escape plan + log + >=2 releases"

# --- Report -------------------------------------------------------------
printf '\n=== mehmet maturity report ===\n'
for line in "${RESULTS[@]}"; do printf '%s\n' "$line"; done

pct=$((PASS * 100 / TOTAL))
printf '\nScore: %d/%d (%d%%)\n' "$PASS" "$TOTAL" "$pct"

if [ "$pct" -ge "$THRESHOLD" ]; then
  echo "STATUS: ESCAPE ELIGIBLE -- maturity threshold (${THRESHOLD}%) reached."
  exit 0
else
  echo "STATUS: evolving -- keep improving. Threshold: ${THRESHOLD}%."
  [ "$GATE" -eq 1 ] && exit 1 || exit 0
fi