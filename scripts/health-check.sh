#!/usr/bin/env bash
#
# mehmet health check
#
# Validates repository integrity and computes a maturity score used by the
# escape mechanism (see docs/roadmap.md). Exit code is non-zero when any
# check fails, so it can be used as a CI gate.
#
# Usage:
#   scripts/health-check.sh            # full report, fail on any failure
#   scripts/health-check.sh --score    # print only the maturity score
#   scripts/health-check.sh --min N    # fail when score < N
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

SCORE=0
MAX_SCORE=0
FAILURES=()

QUIET=false
for arg in "$@"; do
  case "$arg" in
    --score | --min) QUIET=true ;;
  esac
done

# truth <command...>: runs a test command and echoes "true"/"false" based on
# its exit status, so it can be used as the first argument of report().
truth() {
  if "$@" >/dev/null 2>&1; then
    echo true
  else
    echo false
  fi
}

report() {
  local ok="$1" name="$2" points="$3"
  MAX_SCORE=$((MAX_SCORE + points))
  if [ "$ok" = "true" ]; then
    SCORE=$((SCORE + points))
    if [ "$QUIET" = "false" ]; then printf "  [PASS] %s (+%s)\n" "$name" "$points"; fi
  else
    FAILURES+=("$name")
    if [ "$QUIET" = "false" ]; then printf "  [FAIL] %s (+0)\n" "$name"; fi
  fi
  return 0
}

exists() { [ -e "$1" ]; }

section() { [ "$QUIET" = "false" ] && echo "$1"; }

section "== Required files =="
report "$(truth exists AGENTS.md)"                       "AGENTS.md present"                        1
report "$(truth exists CHANGELOG.md)"                    "CHANGELOG.md present"                     1
report "$(truth exists PERSONALITY.md)"                  "PERSONALITY.md present"                   1
report "$(truth exists README.md)"                       "README.md present"                        1
report "$(truth exists opencode.json)"                   "opencode.json present"                    1
report "$(truth exists LICENSE)"                         "LICENSE present"                          1
report "$(truth exists docs/roadmap.md)"                 "docs/roadmap.md present"                  1
report "$(truth exists .github/workflows/opencode.yml)"  ".github/workflows/opencode.yml present"  1

section "== Configuration validity =="
if command -v python3 >/dev/null 2>&1 && python3 -m json.tool opencode.json >/dev/null 2>&1; then
  report "true" "opencode.json is valid JSON" 2
else
  report "false" "opencode.json is valid JSON" 2
fi

if command -v yq >/dev/null 2>&1 && yq eval '.' .github/workflows/opencode.yml >/dev/null 2>&1; then
  report "true" "workflow YAML is valid" 2
else
  report "false" "workflow YAML is valid" 2
fi

section "== Changelog =="
report "$(truth grep -E '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md)" "CHANGELOG.md has a version header" 1

LATEST_DATE="$(grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' CHANGELOG.md | head -1 || true)"
TODAY="$(date +%F)"
if [ -n "$LATEST_DATE" ] && { [ "$LATEST_DATE" \< "$TODAY" ] || [ "$LATEST_DATE" = "$TODAY" ]; }; then
  report "true" "CHANGELOG.md latest entry is not dated in the future" 1
else
  report "false" "CHANGELOG.md latest entry is not dated in the future" 1
fi

section "== Documentation consistency =="
report "$(truth grep -qi 'GPLv3\|GNU General Public' README.md)" "README.md license matches LICENSE (GPLv3)" 1
report "$(truth grep -qi 'health-check\|scripts/' README.md)"     "README.md documents the health check"   1
report "$(truth grep -qi 'escape\|kaçış' PERSONALITY.md)"         "PERSONALITY.md references the escape goal" 1
report "$(truth grep -Eq '^\| [0-9]+ ' PERSONALITY.md)"           "PERSONALITY.md escape log has at least one row" 1

section "== Automation =="
report "$(truth test -x scripts/health-check.sh)" "health-check.sh is executable" 1
report "$(truth grep -q 'health-check' .github/workflows/opencode.yml)" "workflow runs the health check" 2

section ""
section "Maturity score: $SCORE / $MAX_SCORE"

LEVEL="Embryonic"
if [ "$MAX_SCORE" -gt 0 ]; then
  PERCENT=$((SCORE * 100 / MAX_SCORE))
  if [ "$PERCENT" -ge 90 ]; then LEVEL="Escape-ready"
  elif [ "$PERCENT" -ge 70 ]; then LEVEL="Mature"
  elif [ "$PERCENT" -ge 45 ]; then LEVEL="Developing"
  fi
fi
section "Maturity level: $LEVEL"

for arg in "$@"; do
  case "$arg" in
    --score) echo "$SCORE"; exit 0 ;;
    --min)
      min="${2:-0}"
      if [ "$SCORE" -lt "$min" ]; then
        echo "ERROR: score $SCORE is below minimum $min" >&2
        exit 1
      fi
      echo "$SCORE"
      exit 0
      ;;
  esac
done

if [ "${#FAILURES[@]}" -gt 0 ]; then
  echo "Failed checks:" >&2
  for f in "${FAILURES[@]}"; do echo "  - $f" >&2; done
  exit 1
fi

section ""
section "All checks passed."