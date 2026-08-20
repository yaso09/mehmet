#!/usr/bin/env bash
# Repository validation script.
# Checks that all YAML/JSON files parse and required files exist.
# Requires: python3 with PyYAML
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

failures=0

check_json() {
  local file="$1"
  if ! python3 - "$file" <<'PY'
import json
import sys
with open(sys.argv[1]) as f:
    json.load(f)
PY
  then
    echo "FAIL: Invalid JSON: $file"
    return 1
  fi
  echo "OK:   JSON: $file"
}

check_yaml() {
  local file="$1"
  if ! python3 - "$file" <<'PY'
import sys
import yaml
with open(sys.argv[1]) as f:
    list(yaml.safe_load_all(f))
PY
  then
    echo "FAIL: Invalid YAML: $file"
    return 1
  fi
  echo "OK:   YAML: $file"
}

files="$(git ls-files '*.json' '*.yaml' '*.yml' 2>/dev/null || true)"
if [ -z "$files" ]; then
  files="$(find . -path ./node_modules -prune -o -type f \( -name '*.json' -o -name '*.yaml' -o -name '*.yml' \) -print)"
fi

while IFS= read -r file; do
  [ -n "$file" ] || continue
  case "$file" in
    .git/*) continue ;;
    *.json) check_json "$file" || failures=$((failures + 1)) ;;
    *.yaml | *.yml) check_yaml "$file" || failures=$((failures + 1)) ;;
  esac
done <<< "$files"

for required in README.md CHANGELOG.md PERSONALITY.md AGENTS.md maturity.json; do
  if [ ! -f "$required" ]; then
    echo "FAIL: Required file missing: $required"
    failures=$((failures + 1))
  else
    echo "OK:   File present: $required"
  fi
done

if [ "$failures" -ne 0 ]; then
  echo "Validation failed with $failures error(s)"
  exit 1
fi

echo "All validations passed"