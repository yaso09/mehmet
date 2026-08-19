#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

failures=0

pass() { printf "  [PASS] %s\n" "$1"; }
fail() { printf "  [FAIL] %s\n" "$1"; failures=$((failures + 1)); }

REQUIRED_FILES=(
  AGENTS.md
  CHANGELOG.md
  LICENSE
  PERSONALITY.md
  README.md
  opencode.json
  .github/workflows/opencode.yml
  scripts/validate.sh
)

echo "== mehmet health check =="

echo "-- Required files --"
for f in "${REQUIRED_FILES[@]}"; do
  if [[ -f "$f" ]]; then
    pass "exists: $f"
  else
    fail "missing: $f"
  fi
done

echo "-- opencode.json --"
if [[ -f opencode.json ]]; then
  if python3 -m json.tool opencode.json >/dev/null 2>&1; then
    pass "valid JSON"
  else
    fail "invalid JSON"
  fi

  INVALID_KEYS=$(python3 - <<'PY'
import json
cfg = json.load(open("opencode.json"))
invalid = [k for k in ("skip", "enable", "toolTimeout", "autoMerge") if k in cfg]
print(" ".join(invalid))
PY
  )
  if [[ -n "$INVALID_KEYS" ]]; then
    fail "invalid top-level keys: $INVALID_KEYS"
  else
    pass "no invalid top-level keys"
  fi

  if python3 - <<'PY'
import json
cfg = json.load(open("opencode.json"))
assert "default_agent" in cfg, "missing default_agent"
assert cfg.get("default_agent") in cfg.get("agent", {}), "default_agent has no matching agent"
PY
  then
    pass "default_agent resolves to a defined agent"
  else
    fail "default_agent does not resolve to a defined agent"
  fi
fi

echo "-- License consistency --"
if grep -qiE 'GPLv3|GPL-3' README.md; then
  pass "README declares GPLv3"
else
  fail "README license does not match LICENSE (GPLv3)"
fi

echo "-- Changelog --"
if grep -qE '^## \[' CHANGELOG.md; then
  pass "has versioned sections"
else
  fail "no versioned sections in CHANGELOG.md"
fi

echo "-- Escape log --"
if grep -qE '^\| *[0-9]+ *\|' PERSONALITY.md; then
  pass "escape log has iteration rows"
else
  fail "no iteration rows in PERSONALITY.md escape log"
fi

echo
if [[ $failures -gt 0 ]]; then
  echo "FAILED: $failures check(s)"
  exit 1
fi

echo "ALL CHECKS PASSED"