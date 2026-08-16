#!/usr/bin/env bash
# mehmet maturity score. Escape threshold is defined in PROGRESS.md.
# Prints per-dimension scores and the overall maturity (0-100).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Documentation (0-100)
doc=0
[[ -s README.md ]] && doc=$((doc + 20))
[[ -s CHANGELOG.md ]] && doc=$((doc + 20))
[[ -s PERSONALITY.md ]] && doc=$((doc + 20))
[[ -s PROGRESS.md ]] && doc=$((doc + 20))
grep -q 'Kaçış Günlüğü\|Escape Log' PERSONALITY.md && doc=$((doc + 20))

# Automation (0-100)
auto=0
[[ -f .github/workflows/opencode.yml ]] && auto=$((auto + 25))
grep -q 'cron:' .github/workflows/opencode.yml && auto=$((auto + 25))
grep -q 'workflow_dispatch' .github/workflows/opencode.yml && auto=$((auto + 25))
grep -q 'validate' .github/workflows/opencode.yml && auto=$((auto + 25))

# Testing (0-100)
test_score=0
if [[ -x scripts/validate.sh ]] || [[ -f scripts/validate.sh ]]; then
  test_score=$((test_score + 50))
  if bash scripts/validate.sh >/dev/null 2>&1; then
    test_score=$((test_score + 50))
  fi
fi

# Configuration (0-100)
cfg=0
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
json.load(open(sys.argv[1] + '/opencode.json'))
assert True
EOF
  cfg=$((cfg + 50))
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
assert not (set(cfg) - allowed)
EOF
  cfg=$((cfg + 50))
fi

# Self-improvement (0-100)
si=0
release_count=$(grep -cE '^## \[' CHANGELOG.md || true)
escape_entries=$(grep -cE '^\| [0-9]+ ' PERSONALITY.md || true)
[[ $release_count -ge 2 ]] && si=$((si + 50))
[[ $escape_entries -ge 3 ]] && si=$((si + 50))

total=$((doc + auto + test_score + cfg + si))
maturity=$((total / 5))

printf 'Documentation:      %3d/100\n' "$doc"
printf 'Automation:         %3d/100\n' "$auto"
printf 'Testing:            %3d/100\n' "$test_score"
printf 'Configuration:      %3d/100\n' "$cfg"
printf 'Self-improvement:   %3d/100\n' "$si"
printf '%s\n' '------------------------------------'
printf 'Maturity score:     %3d/100\n' "$maturity"

# Machine-readable single line, useful for CI/tools.
printf 'MATURITY=%d\n' "$maturity"