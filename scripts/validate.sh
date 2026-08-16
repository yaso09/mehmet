#!/usr/bin/env bash
# mehmet repo health check. Exit 0 on success, 1 on any failure.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

failures=0
pass() { printf '  [ok] %s\n' "$1"; }
fail() { printf '  [FAIL] %s\n' "$1"; failures=$((failures + 1)); }

echo "== mehmet validation =="

echo "[1] Required files"
required=(
  AGENTS.md
  CHANGELOG.md
  PERSONALITY.md
  PROGRESS.md
  README.md
  opencode.json
  .github/workflows/opencode.yml
  scripts/validate.sh
  scripts/maturity.sh
)
for f in "${required[@]}"; do
  if [[ -f "$f" ]]; then pass "exists: $f"; else fail "missing: $f"; fi
done

echo "[2] opencode.json must be valid JSON and use only schema keys"
if command -v python3 >/dev/null 2>&1; then
  if python3 -c "import json; json.load(open('opencode.json'))" 2>/dev/null; then
    pass "valid JSON"
  else
    fail "invalid JSON"
  fi
  if python3 - "$ROOT" <<'EOF' 2>/dev/null; then
import json, sys
allowed = {
    '$schema', 'shell', 'logLevel', 'server', 'command', 'skills', 'references',
    'reference', 'watcher', 'snapshot', 'plugin', 'share', 'autoshare',
    'autoupdate', 'disabled_providers', 'enabled_providers', 'model',
    'small_model', 'default_agent', 'subagent_depth', 'username', 'mode',
    'agent', 'provider', 'mcp', 'formatter', 'lsp', 'instructions', 'layout',
    'permission', 'tools', 'attachment', 'enterprise', 'tool_output',
    'compaction', 'experimental',
}
cfg = json.load(open(sys.argv[1] + '/opencode.json'))
unknown = set(cfg) - allowed
assert not unknown, 'unknown keys: %s' % sorted(unknown)
EOF
    pass "only schema keys"
  else
    fail "contains unknown top-level keys"
  fi
else
  fail "python3 not available (required for JSON checks)"
fi

echo "[3] CHANGELOG.md must have version headers"
if grep -Eq '^## \[' CHANGELOG.md; then pass "has version headers"; else fail "missing version headers"; fi

echo "[4] PERSONALITY.md must have an escape log"
if grep -q 'Kaçış Günlüğü\|Escape Log' PERSONALITY.md; then pass "has escape log"; else fail "missing escape log"; fi

echo "[5] PROGRESS.md must have a maturity score"
if grep -Eq 'Olgunluk|Maturity|maturity' PROGRESS.md; then pass "has maturity tracking"; else fail "missing maturity tracking"; fi

echo "[6] Docs must be non-empty"
for f in README.md CHANGELOG.md PERSONALITY.md; do
  if [[ -s "$f" ]]; then pass "non-empty: $f"; else fail "empty: $f"; fi
done

echo
if [[ $failures -gt 0 ]]; then
  echo "FAILED: $failures check(s) failed"
  exit 1
fi
echo "ALL CHECKS PASSED"