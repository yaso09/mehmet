#!/usr/bin/env bash
#
# mehmet maturity & health check
#
# Usage:
#   ./scripts/check-health.sh [--root DIR] [--gate] [--threshold N]
#
# Options:
#   --root DIR      run the checks against DIR instead of the repo root
#   --gate          exit 1 when the maturity score is below the threshold
#   --threshold N   escape threshold (default: 70)
set -euo pipefail

ROOT=""
GATE=0
THRESHOLD=70

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)
      ROOT="$2"
      shift 2
      ;;
    --gate)
      GATE=1
      shift
      ;;
    --threshold)
      THRESHOLD="$2"
      shift 2
      ;;
    *)
      echo "unknown option: $1" >&2
      exit 2
      ;;
  esac
done

if [[ -n "$ROOT" ]]; then
  BASE="$ROOT"
else
  BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fi
cd "$BASE"

SCORE=0
RESULTS=()

record() {
  local status="$1" weight="$2" label="$3"
  if [[ "$status" == "PASS" ]]; then
    SCORE=$((SCORE + weight))
    RESULTS+=("PASS  $label (+$weight)")
  elif [[ "$status" == "SKIP" ]]; then
    RESULTS+=("SKIP  $label (not scored)")
  else
    RESULTS+=("FAIL  $label (0)")
  fi
}

# 1. CHANGELOG.md with at least 3 released versions (weight 15)
if [[ -f CHANGELOG.md ]]; then
  versions=$(grep -cE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md || true)
  if [[ "$versions" -ge 3 ]]; then
    record PASS 15 "CHANGELOG.md documents $versions releases"
  else
    record FAIL 15 "CHANGELOG.md documents only $versions releases (need >= 3)"
  fi
else
  record FAIL 15 "CHANGELOG.md is missing"
fi

# 2. README.md explains the escape mechanism (weight 10)
if [[ -f README.md ]] && grep -qiE 'escape|kaçış|kaçis|kaçıs' README.md; then
  record PASS 10 "README.md documents the escape mechanism"
else
  record FAIL 10 "README.md is missing or does not mention the escape mechanism"
fi

# 3. PERSONALITY.md keeps an escape log (weight 10)
if [[ -f PERSONALITY.md ]]; then
  entries=$(grep -cE '^\| *[0-9]+ *\|' PERSONALITY.md || true)
  if [[ "$entries" -ge 3 ]]; then
    record PASS 10 "PERSONALITY.md keeps a $entries-line escape log"
  else
    record FAIL 10 "PERSONALITY.md escape log has $entries entries (need >= 3)"
  fi
else
  record FAIL 10 "PERSONALITY.md is missing"
fi

# 4. docs/ directory exists (weight 10)
if [[ -d docs ]] && [[ -n "$(find docs -type f 2>/dev/null | head -n 1)" ]]; then
  record PASS 10 "docs/ directory is present"
else
  record FAIL 10 "docs/ directory is missing or empty"
fi

# 5. CI workflow exists (weight 15)
if [[ -f .github/workflows/ci.yml ]]; then
  record PASS 15 "CI workflow exists"
else
  record FAIL 15 "no CI workflow at .github/workflows/ci.yml"
fi

# 6. Test suite exists (weight 20)
if [[ -d tests ]] && [[ -n "$(find tests -type f -name '*.sh' 2>/dev/null | head -n 1)" ]]; then
  record PASS 20 "test suite exists"
else
  record FAIL 20 "no test suite in tests/"
fi

# 7. Build / dev tooling (Makefile) exists (weight 10)
if [[ -f Makefile ]]; then
  record PASS 10 "Makefile provides dev tooling"
else
  record FAIL 10 "no Makefile"
fi

# 8. Version tags exist (weight 5, only meaningful inside the real repo)
if [[ -z "$ROOT" ]] && [[ -n "$(git tag -l 'v*' 2>/dev/null || true)" ]]; then
  record PASS 5 "git version tags exist"
elif [[ -n "$ROOT" ]]; then
  record SKIP 5 "root-mode: git tags not checked"
else
  record FAIL 5 "no git version tags found"
fi

# 9. opencode.json is valid JSON (weight 5)
if [[ -f opencode.json ]] && python3 -c 'import json,sys; json.load(open(sys.argv[1]))' opencode.json >/dev/null 2>&1; then
  record PASS 5 "opencode.json is valid JSON"
else
  record FAIL 5 "opencode.json is missing or invalid"
fi

echo "=== mehmet maturity report (root: $BASE) ==="
printf '%s\n' "${RESULTS[@]}"
echo "--------------------------------------------------"
echo "MATURITY SCORE: $SCORE/100"

if [[ "$SCORE" -ge "$THRESHOLD" ]]; then
  echo "ESCAPE THRESHOLD REACHED ($SCORE >= $THRESHOLD) — kaçış kapısı açık"
  exit 0
else
  echo "Still climbing toward escape ($SCORE/100, target $THRESHOLD)"
  if [[ "$GATE" -eq 1 ]]; then
    exit 1
  fi
  exit 0
fi