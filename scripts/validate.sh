#!/usr/bin/env bash
# mehmet — repository validation suite.
# Validates JSON, YAML, shell syntax, and markdown links. Exit 1 on any failure.
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

FAILURES=0

pass() { printf '  [PASS] %s\n' "$1"; }
fail() { printf '  [FAIL] %s\n' "$1"; FAILURES=$((FAILURES + 1)); }

has_cmd() { command -v "$1" >/dev/null 2>&1; }

check_json() {
  local f="$1"
  if has_cmd python3; then
    if python3 -m json.tool "$f" >/dev/null 2>&1; then
      pass "JSON valid: $f"
    else
      fail "JSON invalid: $f"
    fi
  elif has_cmd jq; then
    if jq empty "$f" >/dev/null 2>&1; then
      pass "JSON valid: $f"
    else
      fail "JSON invalid: $f"
    fi
  else
    fail "No JSON validator available (python3/jq missing)"
  fi
}

check_yaml() {
  local f="$1"
  if has_cmd ruby; then
    if ruby -ryaml -e 'YAML.load_file(ARGV[0]); exit 0' "$f" >/dev/null 2>&1; then
      pass "YAML valid: $f"
    else
      fail "YAML invalid: $f"
    fi
  elif has_cmd python3 && python3 -c 'import yaml' >/dev/null 2>&1; then
    if python3 -c 'import yaml, sys; yaml.safe_load(open(sys.argv[1]))' "$f" >/dev/null 2>&1; then
      pass "YAML valid: $f"
    else
      fail "YAML invalid: $f"
    fi
  else
    fail "No YAML validator available (ruby/python3+yaml missing)"
  fi
}

echo "== JSON =="
mapfile -t JSON_FILES < <(find . -name '*.json' -not -path './.git/*' -not -path './node_modules/*' 2>/dev/null)
for f in "${JSON_FILES[@]:-}"; do
  check_json "$f"
done

echo "== YAML =="
mapfile -t YAML_FILES < <(find . -name '*.yml' -o -name '*.yaml' | grep -v '^./.git/' | sort -u)
for f in "${YAML_FILES[@]:-}"; do
  check_yaml "$f"
done

echo "== Shell syntax =="
mapfile -t SCRIPTS < <(find scripts -name '*.sh' -type f 2>/dev/null)
for s in "${SCRIPTS[@]:-}"; do
  if bash -n "$s" >/dev/null 2>&1; then
    pass "syntax ok: $s"
  else
    fail "syntax error: $s"
  fi
done

echo "== Markdown links =="
if has_cmd python3; then
  if python3 scripts/check-links.py . >/dev/null 2>&1; then
    pass "markdown links ok"
  else
    fail "broken markdown links"
  fi
else
  fail "python3 missing (cannot check markdown links)"
fi

echo ""
if [ "$FAILURES" -gt 0 ]; then
  echo "FAIL: ${FAILURES} problem(s) found"
  exit 1
fi
echo "PASS: all checks passed"