#!/usr/bin/env bash
#
# test_project.sh — integrity checks for the mehmet project.
#
# Each check is a small self-contained assertion. A failure is reported
# and the script exits non-zero so CI can act as a quality gate.
#
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PASS=0
FAIL=0

report() { # status name
  if [ "$1" = "ok" ]; then
    PASS=$((PASS + 1))
    printf '  ok   %s\n' "$2"
  else
    FAIL=$((FAIL + 1))
    printf '  FAIL %s\n' "$2"
  fi
}

assert_file() {
  if [ -e "$1" ]; then report ok "file exists: $1"; else report fail "file exists: $1"; fi
}

assert_grep() { # file pattern
  if grep -qE "$2" "$1" 2>/dev/null; then
    report ok "grep '$2' in $1"
  else
    report fail "grep '$2' in $1"
  fi
}

section() { printf '\n== %s ==\n' "$1"; }

section "Required files"
for f in README.md AGENTS.md CHANGELOG.md PERSONALITY.md LICENSE opencode.json .gitignore; do
  assert_file "$f"
done
assert_file ".github/workflows/opencode.yml"

section "Config validity"
if python3 -c "import json; json.load(open('opencode.json'))" 2>/dev/null; then
  report ok "opencode.json is valid JSON"
else
  report fail "opencode.json is valid JSON"
fi
if python3 -c "import yaml,sys; yaml.safe_load(open('.github/workflows/opencode.yml'))" 2>/dev/null; then
  report ok "opencode.yml is valid YAML"
else
  report fail "opencode.yml is valid YAML"
fi

section "Documentation"
assert_grep "README.md" "Özellikler|Features"
assert_grep "README.md" "GPL|Lisans|License"
assert_grep "AGENTS.md" "Kurallar|Rules"
assert_grep "CHANGELOG.md" "^## \["
assert_file "docs/superpowers/specs"

section "Evolution"
assert_grep "PERSONALITY.md" "Kaçış Günlüğü|Escape Log"

section "Automation"
assert_grep ".github/workflows/opencode.yml" "schedule"
assert_grep ".github/workflows/opencode.yml" "OPENCODE_API_KEY"

printf '\n--------------------------------------\n'
printf 'Tests passed: %d   Failed: %d\n' "$PASS" "$FAIL"
printf -- '%s\n' '--------------------------------------'

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
exit 0