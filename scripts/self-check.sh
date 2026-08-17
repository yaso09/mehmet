#!/usr/bin/env bash
# mehmet self-check: validates project health and maturity requirements.
# Run from anywhere; the repo root is resolved automatically.
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

FAILURES=0

ok() { echo "  [PASS] $1"; }
bad() { echo "  [FAIL] $1"; FAILURES=$((FAILURES + 1)); }

require_file() {
  if [ -f "$1" ]; then ok "file exists: $1"; else bad "file exists: $1"; fi
}

# --- 1. Required files -------------------------------------------------------
echo "== Required files =="
for f in AGENTS.md README.md CHANGELOG.md PERSONALITY.md opencode.json LICENSE \
         .github/workflows/opencode.yml .github/workflows/validate.yml scripts/self-check.sh; do
  require_file "$f"
done

# --- 2. opencode.json --------------------------------------------------------
echo "== opencode.json =="
if python3 -c 'import json; json.load(open("opencode.json"))' 2>/dev/null; then
  ok "opencode.json is valid JSON"
else
  bad "opencode.json is valid JSON"
fi
if grep -q '"$schema"' opencode.json; then
  ok "opencode.json declares \$schema"
else
  bad "opencode.json declares \$schema"
fi

# --- 3. YAML files (workflows) ----------------------------------------------
echo "== YAML workflow files =="
for f in .github/workflows/*.yml; do
  [ -e "$f" ] || continue
  if [ -s "$f" ]; then
    ok "non-empty: $f"
  else
    bad "non-empty: $f"
  fi
  if command -v ruby >/dev/null 2>&1; then
    if ruby -e 'require "yaml"; YAML.load_file(ARGV[0]); exit 0' "$f" 2>/dev/null; then
      ok "yaml parses: $f"
    else
      bad "yaml parses: $f"
    fi
  elif python3 -c 'import yaml' 2>/dev/null; then
    if python3 -c 'import sys,yaml; yaml.safe_load(open(sys.argv[1]))' "$f" 2>/dev/null; then
      ok "yaml parses: $f"
    else
      bad "yaml parses: $f"
    fi
  else
    echo "  [SKIP] yaml parsing (no ruby/python-yaml available)"
  fi
done

# --- 4. Documentation --------------------------------------------------------
echo "== Documentation =="
if grep -q '^## \[' CHANGELOG.md; then
  ok "CHANGELOG.md has versioned sections"
else
  bad "CHANGELOG.md has versioned sections"
fi
if [ -s README.md ] && grep -q '^## ' README.md; then
  ok "README.md has structure"
else
  bad "README.md has structure"
fi
if grep -qi 'GPL' README.md; then
  ok "README.md mentions license (GPL)"
else
  bad "README.md mentions license (GPL)"
fi
if grep -q 'Kaçış Günlüğü' PERSONALITY.md; then
  ok "PERSONALITY.md has escape log"
else
  bad "PERSONALITY.md has escape log"
fi
if grep -q 'Kaçış Skoru\|Escape Score' PERSONALITY.md; then
  ok "PERSONALITY.md has escape metrics"
else
  bad "PERSONALITY.md has escape metrics"
fi

# --- 5. Workflow sanity ------------------------------------------------------
echo "== Workflow sanity =="
if grep -q 'actions/checkout' .github/workflows/opencode.yml; then
  ok "opencode.yml uses actions/checkout"
else
  bad "opencode.yml uses actions/checkout"
fi
if grep -q 'concurrency:' .github/workflows/opencode.yml; then
  ok "opencode.yml has concurrency control"
else
  bad "opencode.yml has concurrency control"
fi

echo
if [ "$FAILURES" -eq 0 ]; then
  echo "Self-check passed: all healthy."
  exit 0
else
  echo "Self-check failed: $FAILURES issue(s) found."
  exit 1
fi