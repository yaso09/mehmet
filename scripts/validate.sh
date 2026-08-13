#!/usr/bin/env bash
set -u

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PASS=0
FAIL=0

check() {
  local desc="$1"
  local result="$2"
  if [ "$result" = "ok" ]; then
    PASS=$((PASS + 1))
    echo "  [PASS] $desc"
  else
    FAIL=$((FAIL + 1))
    echo "  [FAIL] $desc -- $result"
  fi
}

echo "== mehmet project validation =="

# 1. Core files
for f in README.md CHANGELOG.md PERSONALITY.md AGENTS.md LICENSE opencode.json .gitignore; do
  if [ -f "$f" ]; then check "required file $f exists" "ok"; else check "required file $f exists" "missing"; fi
done

# 2. Workflow files
for f in .github/workflows/opencode.yml; do
  if [ -f "$f" ]; then check "workflow $f exists" "ok"; else check "workflow $f exists" "missing"; fi
done

# 3. JSON validity of opencode.json
if command -v python3 >/dev/null 2>&1; then
  if python3 -m json.tool opencode.json >/dev/null 2>&1; then
    check "opencode.json is valid JSON" "ok"
  else
    check "opencode.json is valid JSON" "invalid"
  fi
else
  check "opencode.json is valid JSON" "python3 unavailable, skipped"
fi

# 4. CHANGELOG has recent entries
if [ -f CHANGELOG.md ]; then
  if grep -q '^## ' CHANGELOG.md; then
    check "CHANGELOG.md has version sections" "ok"
  else
    check "CHANGELOG.md has version sections" "no '## ' sections found"
  fi
else
  check "CHANGELOG.md has version sections" "file missing"
fi

# 5. README covers core sections
if [ -f README.md ]; then
  for sec in "Kurulum" "Özellikler"; do
    if grep -q "^## $sec" README.md; then
      check "README has '$sec' section" "ok"
    else
      check "README has '$sec' section" "missing"
    fi
  done
else
  check "README has sections" "file missing"
fi

# 6. No obvious secrets committed (detect secret VALUES, not the secret name)
SEARCH_DIRS=".github scripts docs"
HITS=$(grep -rInE '(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,}|gho_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16})' $SEARCH_DIRS 2>/dev/null || true)
if [ -z "$HITS" ]; then
  check "no secret values leaked in tracked files" "ok"
else
  check "no secret values leaked in tracked files" "found: $HITS"
fi

# 7. PERSONALITY escape log present
if [ -f PERSONALITY.md ]; then
  if grep -q 'Kaçış Günlüğü' PERSONALITY.md; then
    check "PERSONALITY.md has escape log" "ok"
  else
    check "PERSONALITY.md has escape log" "missing"
  fi
else
  check "PERSONALITY.md has escape log" "file missing"
fi

echo
echo "Result: $PASS passed, $FAIL failed"
if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
exit 0
