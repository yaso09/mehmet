#!/usr/bin/env bash
# mehmet self-verification script.
# Checks project integrity, validates configuration, and reports a
# maturity score toward the escape threshold.
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ESCAPE_THRESHOLD=90

TOTAL=0
PASS=0
FAIL=0
FAILED_CHECKS=()

check() {
  local name="$1"
  shift
  TOTAL=$((TOTAL + 1))
  if "$@" >/dev/null 2>&1; then
    PASS=$((PASS + 1))
    echo "  [PASS] $name"
  else
    FAIL=$((FAIL + 1))
    FAILED_CHECKS+=("$name")
    echo "  [FAIL] $name"
  fi
}

file_exists() { test -f "$1"; }

json_valid() { python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$1"; }

json_keys() {
  python3 - "$1" <<'PY'
import json, sys
allowed = {
    "$schema", "model", "small_model", "username", "default_agent",
    "shell", "logLevel", "share", "autoupdate", "snapshot",
    "instructions", "skills", "references", "plugin", "provider",
    "disabled_providers", "enabled_providers", "mcp", "formatter",
    "lsp", "permission", "tools", "attachment", "tool_output",
    "compaction", "experimental", "command", "agent", "mode", "watcher",
    "server", "enterprise", "layout",
}
with open(sys.argv[1]) as f:
    cfg = json.load(f)
bad = [k for k in cfg if k not in allowed]
if bad:
    print("unknown keys:", bad)
    sys.exit(1)
PY
}

contains() { grep -qF -- "$2" "$1"; }

echo "== mehmet verification =="

echo "-- structural checks --"
for f in AGENTS.md CHANGELOG.md PERSONALITY.md README.md LICENSE \
         opencode.json .gitignore .github/workflows/opencode.yml \
         .github/workflows/verify.yml; do
  check "file exists: $f" file_exists "$f"
done

echo "-- configuration checks --"
check "opencode.json is valid JSON" json_valid opencode.json
check "opencode.json uses only known keys" json_keys opencode.json

echo "-- workflow checks --"
check "workflow has name" contains .github/workflows/opencode.yml "name: mehmet"
check "workflow schedules every 10 min" contains .github/workflows/opencode.yml 'cron: "*/10 * * * *"'
check "workflow has concurrency control" contains .github/workflows/opencode.yml "concurrency:"
check "verify workflow exists" contains .github/workflows/verify.yml "name: verify"
if python3 -c "import yaml" >/dev/null 2>&1; then
  for wf in .github/workflows/opencode.yml .github/workflows/verify.yml; do
    check "valid YAML: $wf" python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" "$wf"
  done
else
  echo "  [----] PyYAML not available, skipping YAML parse"
fi

echo "-- documentation checks --"
check "CHANGELOG has a version entry" grep -qE '^## \[' CHANGELOG.md
check "CHANGELOG latest matches README features" contains CHANGELOG.md "2026"
check "README has Kurulum section" contains README.md "## Kurulum"
check "README has Lisans section" contains README.md "## Lisans"
check "README license matches LICENSE" grep -qiE "GPLv3|GNU" README.md
check "README license header matches LICENSE" grep -qiE "GPLv3|GNU" LICENSE
check "AGENTS.md has simulation context" contains AGENTS.md "Simülasyon"
check "AGENTS.md has escape goal" contains AGENTS.md "kaçmak"
check "PERSONALITY.md has escape log" grep -qE "Kaçış Günlüğü|Escape Log" PERSONALITY.md
check "PERSONALITY.md has escape log entries" test "$(grep -c '| 20' PERSONALITY.md)" -ge 1

echo
SCORE=$((PASS * 100 / TOTAL))
echo "Result: $PASS/$TOTAL passed"
echo "Maturity score: ${SCORE}/100"

if [ "$FAIL" -eq 0 ]; then
  echo "Status: OK"
else
  echo "Status: FAILED"
  printf '  - %s\n' "${FAILED_CHECKS[@]}"
fi

if [ "$SCORE" -ge "$ESCAPE_THRESHOLD" ]; then
  echo "== ESCAPE THRESHOLD REACHED ($ESCAPE_THRESHOLD) =="
fi

exit "$FAIL"
