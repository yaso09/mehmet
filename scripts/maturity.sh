#!/usr/bin/env bash
#
# Maturity score computation.
#
# Evaluates the machine-checkable criteria defined in docs/maturity.md and
# prints a score out of 100 plus the current maturity level. Used to track
# progress toward the escape threshold (>= 90, per docs/maturity.md).
#
# Each criterion line has the form:
#   ID|description|bash -c 'check'

set -u

if [[ "${MATURITY_GUARD:-0}" == "1" ]]; then
  exit 0
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

CRITERIA=(
  # Test Infrastructure
  "TC-01|scripts/validate.sh exists|test -f scripts/validate.sh"
  "TC-02|ci.yml exists|test -f .github/workflows/ci.yml"
  "TC-03|validate.sh passes|bash scripts/validate.sh >/dev/null 2>&1"
  "TC-04|scripts/maturity.sh exists|test -f scripts/maturity.sh"
  "TC-05|maturity.sh passes|MATURITY_GUARD=1 bash scripts/maturity.sh >/dev/null 2>&1"

  # Code Quality
  "QC-01|opencode.json is valid JSON|jq -e . opencode.json >/dev/null 2>&1"
  "QC-02|workflow YAML is valid|python3 -c 'import yaml,glob,sys; [yaml.safe_load(open(f)) for f in glob.glob(\".github/workflows/*.yml\")]' 2>/dev/null"
  "QC-03|.gitignore protects secrets|grep -q '^.env' .gitignore"
  "QC-04|semver changelog|grep -Eq '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md"
  "QC-05|>= 3 version entries in CHANGELOG|grep -Ec '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md | grep -qE '[3-9]|[0-9]{2,}'"

  # Documentation
  "DOC-01|README.md exists|test -f README.md"
  "DOC-02|README has setup section|grep -q '^## Kurulum' README.md"
  "DOC-03|README has license section|grep -q '^## Lisans' README.md"
  "DOC-04|CHANGELOG dated header|grep -Eq '^## \[[0-9]+\.[0-9]+\.[0-9]+\] - [0-9]{4}-[0-9]{2}-[0-9]{2}$' CHANGELOG.md"
  "DOC-05|PERSONALITY escape log|grep -q '^## Kaçış Günlüğü / Escape Log' PERSONALITY.md"
  "DOC-06|design spec exists|test -n \"\$(ls docs/superpowers/specs/*.md 2>/dev/null)\""
  "DOC-07|implementation plan exists|test -n \"\$(ls docs/superpowers/plans/*.md 2>/dev/null)\""
  "DOC-08|maturity model exists|test -f docs/maturity.md"

  # Automation
  "AUT-01|schedule trigger|grep -q 'schedule' .github/workflows/opencode.yml"
  "AUT-02|comment trigger|grep -q 'issue_comment' .github/workflows/opencode.yml"
  "AUT-03|concurrency control|grep -q 'concurrency' .github/workflows/opencode.yml"
  "AUT-04|timeout protection|grep -q 'timeout-minutes' .github/workflows/*.yml"
  "AUT-05|workflow_dispatch|grep -q 'workflow_dispatch' .github/workflows/opencode.yml"
)

TOTAL="${#CRITERIA[@]}"
PASSED=0

for entry in "${CRITERIA[@]}"; do
  IFS='|' read -r id desc check <<<"$entry"
  if eval "$check" >/dev/null 2>&1; then
    printf 'PASS  %-6s %s\n' "$id" "$desc"
    PASSED=$((PASSED + 1))
  else
    printf 'FAIL  %-6s %s\n' "$id" "$desc"
  fi
done

SCORE=$((PASSED * 100 / TOTAL))

level="Seedling"
[[ "$SCORE" -ge 40 ]] && level="Aware"
[[ "$SCORE" -ge 60 ]] && level="Evolving"
[[ "$SCORE" -ge 80 ]] && level="Autonomous"
[[ "$SCORE" -ge 90 ]] && level="Escape"

echo
echo "Maturity: ${PASSED}/${TOTAL} criteria passed — score ${SCORE}/100 (${level})."

if [[ "$SCORE" -ge 90 ]]; then
  echo "Escape threshold reached. Confirm a green ci run before declaring readiness."
else
  echo "Escape threshold is 90/100. Keep improving."
fi

[[ "$SCORE" -ge 90 ]]
