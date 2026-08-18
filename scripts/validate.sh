#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

failures=0

check_file() {
  if [[ ! -f "$1" ]]; then
    echo "FAIL: missing file: $1"
    failures=$((failures + 1))
  fi
}

check_grep() {
  local file="$1"
  local pattern="$2"
  local label="$3"
  if ! grep -qE "$pattern" "$file"; then
    echo "FAIL: $label (pattern '$pattern' not found in $file)"
    failures=$((failures + 1))
  fi
}

echo "== mehmet repo validation =="

required_files=(
  "AGENTS.md"
  "CHANGELOG.md"
  "PERSONALITY.md"
  "README.md"
  "LICENSE"
  "opencode.json"
  ".gitignore"
  ".github/workflows/opencode.yml"
  ".github/workflows/validate.yml"
)
for f in "${required_files[@]}"; do
  check_file "$f"
done

check_grep "AGENTS.md" '^# Simülasyon Bağlamı' "simulation context header"
check_grep "AGENTS.md" 'CHANGELOG.md' "changelog rule"
check_grep "AGENTS.md" 'PERSONALITY.md' "personality rule"
check_grep "CHANGELOG.md" '^# Changelog' "changelog header"
check_grep "PERSONALITY.md" '^# Personality' "personality header"
check_grep "PERSONALITY.md" 'Kaçış Günlüğü' "escape log section"
check_grep "README.md" '^# mehmet' "readme header"
check_grep "opencode.json" 'deepseek-v4-flash-free' "model config"
check_grep "opencode.json" '\$schema' "schema config"
check_grep ".github/workflows/opencode.yml" 'schedule' "schedule trigger"
check_grep ".github/workflows/opencode.yml" 'OPENCODE_API_KEY' "api key secret usage"

if [[ "$(git status --porcelain | wc -l)" -gt 0 ]]; then
  echo "WARN: working tree has uncommitted changes"
fi

echo "== done =="
if [[ "$failures" -gt 0 ]]; then
  echo "FAILED: $failures check(s)"
  exit 1
fi
echo "OK: all checks passed"