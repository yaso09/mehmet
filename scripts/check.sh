#!/usr/bin/env bash
# mehmet — repository health check.
# Validates config files, required docs and the escape log. Used by CI
# (.github/workflows/validate.yml) and by the agent before committing.
#
# Usage: ./scripts/check.sh
# Exit code 0 = healthy, 1 = problems found.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

failures=0

ok()   { printf '  [ok]   %s\n' "$1"; }
bad()  { printf '  [FAIL] %s\n' "$1"; failures=$((failures + 1)); }

section() { printf '\n== %s ==\n' "$1"; }

section "Required files"
for f in AGENTS.md README.md CHANGELOG.md PERSONALITY.md LICENSE \
         opencode.json docs/escape-mechanism.md .github/workflows/opencode.yml; do
  if [[ -f "$f" ]]; then ok "present: $f"; else bad "missing: $f"; fi
done

section "opencode.json (JSON)"
if jq empty opencode.json 2>/dev/null; then
  ok "valid JSON"
  [[ -n "$(jq -r .model opencode.json)" ]] && ok "model set" || bad "model missing"
else
  bad "invalid JSON"
fi

section "Workflow YAML"
if command -v yamllint >/dev/null 2>&1; then
  if yamllint -d relaxed .github/workflows/opencode.yml >/dev/null 2>&1; then
    ok "opencode.yml syntax"
  else
    bad "opencode.yml syntax"
  fi
elif python3 -c 'import yaml,sys; yaml.safe_load(open(sys.argv[1]))' .github/workflows/opencode.yml 2>/dev/null; then
  ok "opencode.yml syntax"
else
  bad "opencode.yml syntax"
fi

section "Escape log (PERSONALITY.md)"
if [[ -f PERSONALITY.md ]]; then
  if grep -q '^## Kaçış Günlüğü / Escape Log' PERSONALITY.md; then
    ok "escape log section present"
  else
    bad "escape log section missing"
  fi
fi

section "Changelog"
if [[ -f CHANGELOG.md ]]; then
  latest="$(grep -oE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md | head -1 || true)"
  if [[ -n "$latest" ]]; then
    ok "latest release: $latest"
  else
    bad "no semver release header found"
  fi
else
  bad "CHANGELOG.md missing"
fi

section "No stray secrets"
if grep -rnE '(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|OPENCODE_API_KEY\s*=\s*.+)' \
     --include='*.md' --include='*.yml' --include='*.json' --include='*.sh' . 2>/dev/null; then
  bad "possible secret committed"
else
  ok "no secrets found"
fi

if [[ $failures -gt 0 ]]; then
  printf '\nFAILED: %d problem(s) found.\n' "$failures"
  exit 1
fi

printf '\nAll checks passed.\n'