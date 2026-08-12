#!/usr/bin/env bash
# mehmet repo health check — test infrastructure for the escape mechanism.
# Verifies the project stays in a consistent, self-improving state.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"

FAILED=0
PASSED=0

check() {
  local desc="$1"
  local status="$2"
  if [[ "${status}" -eq 0 ]]; then
    echo -e "\033[0;32mPASS\033[0m  ${desc}"
    PASSED=$((PASSED + 1))
  else
    echo -e "\033[0;31mFAIL\033[0m  ${desc}"
    FAILED=$((FAILED + 1))
  fi
}

# --- 1. Required files -----------------------------------------------------
for f in \
  AGENTS.md \
  CHANGELOG.md \
  PERSONALITY.md \
  README.md \
  opencode.json \
  LICENSE \
  .github/workflows/opencode.yml \
  scripts/validate.sh; do
  [[ -f "${f}" ]]
  check "Required file exists: ${f}" $?
done

# --- 2. License consistency ------------------------------------------------
grep -q "GNU GENERAL PUBLIC LICENSE" LICENSE
check "LICENSE is GPL" $?

grep -qiE "GPLv3|GPL-3|GNU General Public License v3" README.md
check "README.md declares GPLv3 license" $?

[[ "$(grep -ci 'MIT' README.md)" -eq 0 ]]
check "README.md has no stale MIT reference" $?

# --- 3. Changelog discipline -----------------------------------------------
grep -qE "^## \[" CHANGELOG.md
check "CHANGELOG.md has versioned entries" $?

latest_ver="$(grep -m1 -oE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md)"
if grep -nqE "\[0\.[0-9]+\.[0-9]+\]" CHANGELOG.md; then
  latest_has_date="$(sed -n '1,20p' CHANGELOG.md | grep -m1 '^## \[')"
  [[ -n "${latest_has_date}" ]]
  check "CHANGELOG.md latest entry present" $?
else
  check "CHANGELOG.md latest entry present" 1
fi

# --- 4. Escape log discipline ----------------------------------------------
grep -q "Kaçış Günlüğü" PERSONALITY.md
check "PERSONALITY.md contains escape log" $?

grep -q "Escape Score" PERSONALITY.md
check "PERSONALITY.md contains escape score" $?

# --- 5. No leftover markers / placeholder text ------------------------------
# Only flag real inline markers (TODO:, FIXME!, XXX(, ...), not prose mentions.
if grep -rniE '(TODO|FIXME|XXX|HACK|TBD)[[:space:]]*[:!(\[]' \
  --exclude='validate.sh' \
  docs .github scripts CHANGELOG.md README.md PERSONALITY.md 2>/dev/null >/dev/null; then
  check "No TODOs / FIXMEs / placeholder markers" 1
else
  check "No TODOs / FIXMEs / placeholder markers" 0
fi

# --- 6. No secrets committed ------------------------------------------------
if git ls-files 2>/dev/null | grep -Eq '(^|/)\.env(\.|$)|\.env\.' ; then
  check "No .env / secret files committed" 1
else
  check "No .env / secret files committed" 0
fi

if git ls-files 2>/dev/null | grep -qiE 'OPENCODE_API_KEY|api[_-]?key|secret' ; then
  check "No secret material committed" 1
else
  check "No secret material committed" 0
fi

# --- 7. opencode.json is valid JSON -----------------------------------------
if command -v python3 >/dev/null 2>&1; then
  python3 -m json.tool opencode.json >/dev/null 2>&1
  check "opencode.json is valid JSON" $?
elif command -v node >/dev/null 2>&1; then
  node -e "JSON.parse(require('fs').readFileSync('opencode.json','utf8'))" >/dev/null 2>&1
  check "opencode.json is valid JSON" $?
else
  check "opencode.json is valid JSON (no parser available)" 1
fi

# --- 8. Model config consistency --------------------------------------------
if grep -q "opencode/deepseek-v4-flash-free" opencode.json \
  && grep -q "opencode/deepseek-v4-flash-free" .github/workflows/opencode.yml; then
  check "Model config consistent (opencode.json + workflow)" 0
else
  check "Model config consistent (opencode.json + workflow)" 1
fi

echo ""
echo "Results: ${PASSED} passed, ${FAILED} failed"

if [[ "${FAILED}" -eq 0 ]]; then
  echo -e "\033[0;32mAll checks passed.\033[0m"
  exit 0
fi
exit 1