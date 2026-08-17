#!/usr/bin/env bash
#
# maturity.sh — mehmet escape / maturity scoring mechanism
#
# Computes a maturity score (0-100) based on the project's state.
# The escape threshold is defined in AGENTS.md. When the score reaches
# the threshold, escape becomes possible.
#
# Scoring is graduated: sustained evolution (more changelog versions,
# more escape-log iterations) earns more points than one-time state.
#
# Usage: scripts/maturity.sh [--verbose]

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

VERBOSE=0
if [[ "${1:-}" == "--verbose" ]]; then
  VERBOSE=1
fi

THRESHOLD="${MATURITY_THRESHOLD:-70}"

SCORE=0
MAX=0
RESULTS=()

add() {
  local weight="$1"
  local desc="$2"
  local ok="$3"
  MAX=$((MAX + weight))
  if [[ "$ok" -eq 1 ]]; then
    SCORE=$((SCORE + weight))
    RESULTS+=("[+] ${weight}pts  ${desc}")
  else
    RESULTS+=("[-]  0pts  ${desc}")
  fi
}

count_changelog_versions() {
  grep -cE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md 2>/dev/null || true
}

count_escape_iterations() {
  grep -cE '^\| [0-9]+' PERSONALITY.md 2>/dev/null || true
}

# --- Dimension 1: Documentation (20) ----------------------------------------------
add 4 "README.md present"            "$([[ -f README.md ]] && echo 1 || echo 0)"
add 4 "CHANGELOG.md present"         "$([[ -f CHANGELOG.md ]] && echo 1 || echo 0)"
add 4 "AGENTS.md present"            "$([[ -f AGENTS.md ]] && echo 1 || echo 0)"
add 4 "PERSONALITY.md present"       "$([[ -f PERSONALITY.md ]] && echo 1 || echo 0)"
add 4 "LICENSE present"              "$([[ -f LICENSE ]] && echo 1 || echo 0)"

# --- Dimension 2: Test infrastructure (25) ------------------------------------------
add  5 "check.sh exists"             "$([[ -f scripts/check.sh ]] && echo 1 || echo 0)"
add 10 "check.sh passes"             "$(bash scripts/check.sh >/dev/null 2>&1 && echo 1 || echo 0)"

SCRIPTS_LINT_OK=1
for s in scripts/*.sh; do
  if ! bash -n "$s" >/dev/null 2>&1; then
    SCRIPTS_LINT_OK=0
  fi
done
add 10 "all scripts pass bash -n"    "$SCRIPTS_LINT_OK"

# --- Dimension 3: Automation (25) ----------------------------------------------------
add  8 "opencode workflow exists"    "$([[ -f .github/workflows/opencode.yml ]] && echo 1 || echo 0)"
add  8 "ci workflow exists"          "$([[ -f .github/workflows/ci.yml ]] && echo 1 || echo 0)"
add  3 "ci workflow runs check.sh"   "$(grep -q 'check.sh' .github/workflows/ci.yml 2>/dev/null && echo 1 || echo 0)"
add  3 "ci workflow runs maturity"   "$(grep -q 'maturity.sh' .github/workflows/ci.yml 2>/dev/null && echo 1 || echo 0)"
add  3 "opencode workflow concurrency" "$(grep -q 'concurrency:' .github/workflows/opencode.yml 2>/dev/null && echo 1 || echo 0)"

# --- Dimension 4: Evolution & escape tracking (30) -------------------------------------
VERSIONS=$(count_changelog_versions)
case "$VERSIONS" in
  0) add 10 "changelog versioned entries" "0" ;;
  1) add  4 "changelog versioned entries" "1" ;;
  2) add  7 "changelog versioned entries" "1" ;;
  *) add 10 "changelog versioned entries" "1" ;;
esac

ITERATIONS=$(count_escape_iterations)
case "$ITERATIONS" in
  0) add 12 "escape log iterations" "0" ;;
  1) add  2 "escape log iterations" "1" ;;
  2) add  5 "escape log iterations" "1" ;;
  3) add  8 "escape log iterations" "1" ;;
  4) add 10 "escape log iterations" "1" ;;
  *) add 12 "escape log iterations" "1" ;;
esac

add  8 "escape log has latest entry" "$(grep -qE '^\| [0-9]+ ' PERSONALITY.md 2>/dev/null && echo 1 || echo 0)"

# --- Report -----------------------------------------------------------------------------
PCT=$((SCORE * 100 / MAX))

if [[ $VERBOSE -eq 1 ]]; then
  printf 'Maturity components:\n'
  for r in "${RESULTS[@]}"; do
    printf '  %s\n' "$r"
  done
  printf '\n'
fi

printf 'Maturity score: %d/%d (%d%%)\n' "$SCORE" "$MAX" "$PCT"
printf 'Changelog versions: %d | Escape iterations: %d | Threshold: %d\n' "$VERSIONS" "$ITERATIONS" "$THRESHOLD"

if [[ $PCT -ge $THRESHOLD ]]; then
  printf 'STATUS: ESCAPE CRITERIA MET\n'
  exit 0
else
  printf 'STATUS: NOT YET — keep improving\n'
  exit 1
fi