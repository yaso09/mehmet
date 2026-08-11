#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

FAILED=0

fail() {
  echo "FAIL: $1"
  FAILED=1
}

ok() {
  echo "OK: $1"
}

require_file() {
  if [ -f "$1" ]; then
    ok "file exists: $1"
  else
    fail "missing required file: $1"
  fi
}

# --- Required files -------------------------------------------------------
for f in AGENTS.md CHANGELOG.md LICENSE PERSONALITY.md README.md VERSION \
    opencode.json .github/workflows/opencode.yml .github/workflows/validate.yml; do
  require_file "$f"
done

# --- JSON config ----------------------------------------------------------
if jq empty opencode.json 2>/dev/null; then
  ok "valid JSON: opencode.json"
else
  fail "invalid JSON: opencode.json"
fi

# --- YAML workflows -------------------------------------------------------
validate_yaml() {
  local f="$1"
  if command -v yq >/dev/null 2>&1; then
    yq eval '.' "$f" >/dev/null 2>&1
  elif command -v ruby >/dev/null 2>&1; then
    ruby -e "require 'yaml'; YAML.load_file('$f')" >/dev/null 2>&1
  elif command -v python3 >/dev/null 2>&1; then
    python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" "$f" >/dev/null 2>&1
  else
    return 1
  fi
}

for f in .github/workflows/opencode.yml .github/workflows/validate.yml; do
  if validate_yaml "$f"; then
    ok "valid YAML: $f"
  else
    fail "invalid YAML: $f"
  fi
done

# --- Version consistency ---------------------------------------------------
VERSION="$(cat VERSION)"
echo "  version in VERSION file: $VERSION"

if grep -q "^## \[$VERSION\]" CHANGELOG.md; then
  ok "CHANGELOG.md has entry for [$VERSION]"
else
  fail "CHANGELOG.md is missing entry for [$VERSION]"
fi

if grep -qE "Version[^0-9]*$VERSION" README.md; then
  ok "README.md references version $VERSION"
else
  fail "README.md does not reference version $VERSION"
fi

# --- Maturity tracker -------------------------------------------------------
if grep -qi "maturity\|olgunluk" MATURITY.md; then
  ok "MATURITY.md contains maturity scoring"
else
  fail "MATURITY.md missing maturity scoring"
fi

# --- Escape log -------------------------------------------------------------
if ! grep -q "| 3 " PERSONALITY.md; then
  fail "PERSONALITY.md escape log has no entry for iteration 3"
fi

echo
if [ "$FAILED" -eq 0 ]; then
  echo "All validation checks passed."
else
  echo "Validation FAILED."
  exit 1
fi
