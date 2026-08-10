#!/usr/bin/env bash
set -euo pipefail

# mehmet — project health validation script
# Usage: ./scripts/check.sh
# Exit codes: 0 = healthy, 1 = validation failed

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PASS=0
FAIL=0

say()  { printf '%-70s' "$1"; }
pass() { printf '[PASS]\n'; ((PASS++)); }
fail() { printf '[FAIL]\n'; ((FAIL++)); return 1; }

note() { printf '%s\n' "  -> $1"; }

echo "== mehmet health check =="
echo

# --- 1. Required files exist -------------------------------------------------
say "required files present"
missing=0
for f in \
  AGENTS.md CHANGELOG.md PERSONALITY.md README.md \
  LICENSE opencode.json .gitignore \
  .github/workflows/opencode.yml \
  scripts/check.sh docs/ESCAPE.md
do
  if [[ ! -e "$ROOT/$f" ]]; then
    note "missing: $f"
    missing=1
  fi
done
if [[ $missing -eq 0 ]]; then pass; else fail; fi

# --- 2. Markdown key sections -------------------------------------------------
say "CHANGELOG has Unreleased or versioned sections"
if grep -qE '^## \[' "$ROOT/CHANGELOG.md"; then pass; else fail; fi

say "CHANGELOG top entry is the latest"
latest=$(grep -oE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' "$ROOT/CHANGELOG.md" | head -1 || true)
if [[ "$latest" =~ \([0-9]+\.[0-9]+\.[0-9]+\) ]]; then pass; else fail; fi

say "PERSONALITY.md has escape log table"
if grep -q '^| Iterasyon' "$ROOT/PERSONALITY.md" && grep -q '^|---' "$ROOT/PERSONALITY.md"; then pass; else fail; fi

say "ESCAPE.md has current score section"
if grep -q '^## Genel' "$ROOT/docs/ESCAPE.md" || grep -qE '^## (Durum|Skor|Current|Score)' "$ROOT/docs/ESCAPE.md"; then pass; else fail; fi

# --- 3. README consistency ---------------------------------------------------
say "README license matches LICENSE"
license_readme=$(grep -oE '(MIT|GPLv3|GPL-3\.0|GPLv2)' "$ROOT/README.md" | head -1 || true)
if grep -q 'GNU GENERAL PUBLIC LICENSE' "$ROOT/LICENSE" && [[ "$license_readme" == "GPLv3" ]]; then pass; else fail; fi
# (MIT fallback: if LICENSE is MIT, require MIT in README)
if ! grep -q 'GNU GENERAL PUBLIC LICENSE' "$ROOT/LICENSE" && [[ "$license_readme" == "MIT" ]]; then pass; fi

# --- 4. JSON/YAML validity ----------------------------------------------------
say "opencode.json is valid JSON"
if jq empty "$ROOT/opencode.json" 2>/dev/null; then pass; else fail; fi

say "workflow YAML is valid"
if [[ "$(command -v yq)" != "" ]]; then
  if yq eval '.' "$ROOT/.github/workflows/opencode.yml" >/dev/null 2>&1; then pass; else fail; fi
else
  if python3 -c 'import yaml,sys; yaml.safe_load(open(sys.argv[1], encoding="utf-8"))' "$ROOT/.github/workflows/opencode.yml" 2>/dev/null; then pass; else fail; fi
fi

# --- 5. No secrets / stray artifacts ------------------------------------------
say "no .env committed"
if [[ ! -e "$ROOT/.env" ]]; then pass; else fail; fi

say "no node_modules committed"
if [[ ! -e "$ROOT/node_modules" ]]; then pass; else fail; fi

say "no *.log files present"
if compgen -G "$ROOT/*.log" >/dev/null; then fail; else pass; fi

# --- 6. Version tags match -----------------------------------------------------
say "ESCAPE score is numeric 0-100"
current=$(awk -F'|' '/^\| (Toplam|Total|Score|Skor)/{gsub(/[[:space:]]/,"",$2); print $2}' "$ROOT/docs/ESCAPE.md" | head -1 | tr -d 'P')
if [[ -n "$current" && "$current" =~ ^[0-9]+$ && $current -ge 0 && $current -le 100 ]]; then
  pass
else fail; fi

echo
echo "== RESULT: $PASS passed, $FAIL failed =="
[[ $FAIL -eq 0 ]] || exit 1