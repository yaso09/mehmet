#!/usr/bin/env bash
#
# Project integrity validator for mehmet.
# Verifies required files exist, JSON/YAML configs are parseable,
# and core documentation is in sync.
#
# Usage: ./scripts/validate.sh
# Exit code 0 = all checks passed, non-zero = failures.

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

PASS=0
FAIL=0

say_ok()   { printf "  \033[32mOK\033[0m    %s\n" "$1"; PASS=$((PASS + 1)); }
say_fail() { printf "  \033[31mFAIL\033[0m  %s\n" "$1"; FAIL=$((FAIL + 1)); }

check_file() {
  local path="$1"
  if [ -f "$path" ]; then
    say_ok "$path exists"
  else
    say_fail "$path is missing"
  fi
}

echo "== Required files =="
for f in AGENTS.md README.md CHANGELOG.md PERSONALITY.md LICENSE opencode.json \
         .github/workflows/opencode.yml scripts/validate.sh; do
  check_file "$f"
done

echo "== JSON validity =="
if jq empty opencode.json 2>/dev/null; then
  say_ok "opencode.json is valid JSON"
else
  say_fail "opencode.json is not valid JSON"
fi

echo "== YAML validity =="
if yq eval '.' .github/workflows/opencode.yml >/dev/null 2>&1; then
  say_ok "opencode.yml is valid YAML"
else
  say_fail "opencode.yml is not valid YAML"
fi

if [ -f .github/workflows/ci.yml ]; then
  if yq eval '.' .github/workflows/ci.yml >/dev/null 2>&1; then
    say_ok "ci.yml is valid YAML"
  else
    say_fail "ci.yml is not valid YAML"
  fi
fi

echo "== Changelog consistency =="
LATEST_VERSION=$(grep -m1 -oE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md | sed 's/^## \[//; s/\]$//')
if [ -z "$LATEST_VERSION" ]; then
  say_fail "CHANGELOG.md has no version headers"
else
  say_ok "CHANGELOG.md latest version: $LATEST_VERSION"
  if ! grep -q "$LATEST_VERSION" README.md; then
    say_fail "README.md does not reference version $LATEST_VERSION"
  else
    say_ok "README.md references version $LATEST_VERSION"
  fi
fi

echo "== Escape log =="
if grep -q '^| ' PERSONALITY.md; then
  say_ok "PERSONALITY.md escape log has entries"
else
  say_fail "PERSONALITY.md escape log is empty"
fi

echo
echo "== Result =="
printf "  passed: %d, failed: %d\n" "$PASS" "$FAIL"
if [ "$FAIL" -gt 0 ]; then
  echo "  FAILURE"
  exit 1
fi
echo "  SUCCESS"
exit 0