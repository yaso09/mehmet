#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

failures=0

ok() {
  printf "  [ok] %s\n" "$1"
}

fail() {
  printf "  [FAIL] %s\n" "$1"
  failures=$((failures + 1))
}

check_file() {
  if [[ -f "$1" ]]; then ok "$1 mevcut"; else fail "$1 eksik"; fi
}

check_grep() {
  local desc="$1" file="$2" pattern="$3"
  if grep -qE "$pattern" "$file" 2>/dev/null; then
    ok "$desc"
  else
    fail "$desc"
  fi
}

printf "mehmet doğrulama / validation\n"
printf -- "----------------------------\n"

check_file "AGENTS.md"
check_file "CHANGELOG.md"
check_file "PERSONALITY.md"
check_file "README.md"
check_file "LICENSE"
check_file "opencode.json"
check_file ".gitignore"
check_file "MATURITY.md"
check_file "scripts/validate.sh"
check_file "scripts/maturity.sh"
check_file ".github/workflows/opencode.yml"
check_file ".github/workflows/validate.yml"

if jq empty opencode.json 2>/dev/null; then
  ok "opencode.json geçerli JSON"
else
  fail "opencode.json geçerli değil"
fi

check_grep "README lisans GPLv3" "README.md" "^GPLv3"
check_grep "README kurulum adımları" "README.md" "^## Kurulum"
check_grep "CHANGELOG sürüm girişi" "CHANGELOG.md" '^## \[[0-9]+\.[0-9]+\.[0-9]+\]'
check_grep "PERSONALITY kaçış günlüğü" "PERSONALITY.md" "Kaçış Günlüğü"
check_grep "LICENSE GPL" "LICENSE" "GNU GENERAL PUBLIC LICENSE"
check_grep "opencode.yml name" ".github/workflows/opencode.yml" "^name:"
check_grep "opencode.yml jobs" ".github/workflows/opencode.yml" "^jobs:"
check_grep "opencode.yml timeout" ".github/workflows/opencode.yml" "timeout-minutes"
check_grep "opencode.yml doğrulama adımı" ".github/workflows/opencode.yml" "validate.sh"
check_grep "opencode.yml sabitlenmiş action" ".github/workflows/opencode.yml" "anomalyco/opencode/github@github-v"
check_grep "validate.yml name" ".github/workflows/validate.yml" "^name:"
check_grep "validate.yml jobs" ".github/workflows/validate.yml" "^jobs:"

if [[ -d .github/ISSUE_TEMPLATE ]]; then
  ok ".github/ISSUE_TEMPLATE mevcut"
else
  fail ".github/ISSUE_TEMPLATE eksik"
fi

printf "\n"

if [[ "$failures" -gt 0 ]]; then
  printf "Doğrulama BAŞARISIZ: %d sorun.\n" "$failures"
  exit 1
fi

printf "Doğrulama başarılı.\n"