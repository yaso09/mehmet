#!/usr/bin/env bash
# mehmet project health verification.
#
# Checks the project's core files, validates config/workflow syntax and
# reports the current escape (maturity) score defined in docs/ESCAPE.md.
# Exits non-zero when any check fails. Used by CI and by mehmet itself.

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

FAILED=0
declare -a WARNINGS=()

say()   { printf '%s\n' "$*"; }
pass()  { say "  [OK]     $*"; }
fail()  { say "  [FAIL]   $*"; FAILED=$((FAILED + 1)); }
warn()  { say "  [WARN]   $*"; WARNINGS+=("$*"); }

check_file() { # check_file <path>
  if [[ -f "$1" ]]; then pass "file present: $1"; else fail "missing file: $1"; fi
}

say ""
say "== Required files =="
check_file "AGENTS.md"
check_file "README.md"
check_file "CHANGELOG.md"
check_file "PERSONALITY.md"
check_file "LICENSE"
check_file "opencode.json"
check_file "CONTRIBUTING.md"
check_file "docs/ESCAPE.md"
check_file "scripts/verify.sh"
check_file ".github/workflows/opencode.yml"
check_file ".github/workflows/verify.yml"

say ""
say "== opencode.json =="
if command -v python3 >/dev/null 2>&1; then
  if python3 -c "import json; json.load(open('opencode.json'))" 2>/dev/null; then
    pass "valid JSON"
  else
    fail "opencode.json is not valid JSON"
  fi
  # The opencode config schema rejects unknown top-level keys, so enforce an
  # allowlist here to catch regressions before opencode hard-fails.
  BAD_KEYS=$(python3 - <<'PY'
import json
allowed = {
    "$schema", "shell", "logLevel", "server", "command", "skills",
    "references", "reference", "watcher", "snapshot", "plugin", "share",
    "autoshare", "autoupdate", "disabled_providers", "enabled_providers",
    "model", "small_model", "default_agent", "subagent_depth", "username",
    "mode", "agent", "provider", "mcp", "formatter", "lsp", "instructions",
    "layout", "permission", "tools", "attachment", "enterprise",
    "tool_output", "compaction", "experimental",
}
data = json.load(open("opencode.json"))
unknown = sorted(k for k in data if k not in allowed)
print(" ".join(unknown))
PY
)
  if [[ -z "$BAD_KEYS" ]]; then
    pass "all top-level keys are valid per opencode config schema"
  else
    fail "invalid top-level keys in opencode.json: $BAD_KEYS"
  fi
else
  warn "python3 not available; skipping JSON validation"
fi

say ""
say "== Workflow YAML =="
if command -v python3 >/dev/null 2>&1 && python3 -c "import yaml" 2>/dev/null; then
  for f in .github/workflows/*.yml; do
    if python3 -c "import sys, yaml; yaml.safe_load(open('$f'))" 2>/dev/null; then
      pass "valid YAML: $f"
    else
      fail "invalid YAML: $f"
    fi
  done
else
  warn "python3 + PyYAML not available; skipping YAML validation"
fi

say ""
say "== Documentation consistency =="
if grep -q "Test-Path\|Get-ChildItem\|Get-Content" docs/superpowers/plans/2026-07-04-mehmet-implementation.md 2>/dev/null; then
  warn "plan doc still references Windows PowerShell commands (project runs on Linux)"
else
  pass "plan doc uses platform-appropriate commands"
fi
if grep -q "2026-08" CHANGELOG.md; then
  pass "CHANGELOG has an entry for the current month"
else
  warn "CHANGELOG has no entry for the current month"
fi

say ""
say "== Maturity / escape status =="
if [[ -f docs/ESCAPE.md ]]; then
  DONE=$(grep -c '^- \[x\]' docs/ESCAPE.md || true)
  TOTAL=$(grep -c '^- \[[ x]\]' docs/ESCAPE.md || true)
  if [[ "$TOTAL" -eq 0 ]]; then
    warn "no escape criteria found in docs/ESCAPE.md"
  else
    pass "maturity score: $DONE/$TOTAL milestones complete"
  fi
else
  warn "docs/ESCAPE.md missing; cannot compute maturity score"
fi

say ""
if [[ ${#WARNINGS[@]} -gt 0 ]]; then
  say "== Warnings ($((${#WARNINGS[@]}))) =="
  for w in "${WARNINGS[@]}"; do say "  - $w"; done
fi

say ""
if [[ "$FAILED" -gt 0 ]]; then
  say "VERIFICATION FAILED: $FAILED check(s) did not pass."
  exit 1
fi
say "VERIFICATION PASSED."
exit 0
