#!/usr/bin/env bash
# mehmet — repository health verification script.
# Validates project structure, config integrity and documentation consistency.
# Exit code 0 when healthy, 1 when any check fails.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PASSES=0
FAILURES=0

report() {
  local status=$1
  local msg=$2
  if [[ "$status" == "PASS" ]]; then
    echo "PASS: $msg"
    ((PASSES += 1))
  else
    echo "FAIL: $msg"
    ((FAILURES += 1))
  fi
}

check_file() {
  if [[ -f "$1" ]]; then
    report "PASS" "$1 exists"
  else
    report "FAIL" "$1 is missing"
  fi
}

check_contains() {
  local file=$1
  local needle=$2
  if [[ -f "$file" ]] && grep -qF -- "$needle" "$file"; then
    report "PASS" "$file contains '$needle'"
  else
    report "FAIL" "$file does not contain '$needle'"
  fi
}

echo "== Project structure =="
for f in AGENTS.md CHANGELOG.md PERSONALITY.md README.md LICENSE opencode.json \
         .gitignore MATURITY.md scripts/verify.sh .github/workflows/opencode.yml .github/workflows/verify.yml; do
  check_file "$f"
done

echo "== Configuration integrity =="
if command -v python3 >/dev/null 2>&1; then
  if python3 -m json.tool opencode.json >/dev/null 2>&1; then
    report "PASS" "opencode.json is valid JSON"
  else
    report "FAIL" "opencode.json is not valid JSON"
  fi
else
  report "FAIL" "python3 not available for JSON validation"
fi

if grep -q '"model"' opencode.json 2>/dev/null; then
  report "PASS" "opencode.json defines a model"
else
  report "FAIL" "opencode.json does not define a model"
fi

echo "== Workflow integrity =="
if grep -q 'OPENCODE_API_KEY' .github/workflows/opencode.yml 2>/dev/null; then
  report "PASS" "opencode.yml references OPENCODE_API_KEY secret"
else
  report "FAIL" "opencode.yml does not reference OPENCODE_API_KEY secret"
fi

if grep -q 'autonomous:' .github/workflows/opencode.yml 2>/dev/null; then
  report "PASS" "opencode.yml has autonomous job"
else
  report "FAIL" "opencode.yml has no autonomous job"
fi

if grep -q 'comment:' .github/workflows/opencode.yml 2>/dev/null; then
  report "PASS" "opencode.yml has comment job"
else
  report "FAIL" "opencode.yml has no comment job"
fi

echo "== Documentation consistency =="
check_contains CHANGELOG.md "0.3.0"
check_contains README.md "Kurulum"
check_contains AGENTS.md "CHANGELOG.md"
check_contains MATURITY.md "Kaçış"

echo "== Security =="
LEAK=$(grep -rInE --exclude-dir=.git --exclude=verify.sh \
  '(sk_live_|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,}|OPENCODE_API_KEY\s*=\s*.{8,})' . 2>/dev/null || true)
if [[ -z "$LEAK" ]]; then
  report "PASS" "no obvious secret patterns found"
else
  report "FAIL" "potential secret leak detected: $LEAK"
fi

echo ""
echo "== Summary: $PASSES passed, $FAILURES failed =="
if [[ "$FAILURES" -gt 0 ]]; then
  exit 1
fi