#!/usr/bin/env bash
#
# mehmet - project integrity & maturity checks
#
# Verifies that the autonomous-agent project is healthy and self-consistent.
# Used both locally (./scripts/check.sh) and in CI (.github/workflows/ci.yml).
#
# Every check is a HARD check: a failure breaks CI and blocks maturity.
# The maturity score (0-100) feeds the escape mechanism described in
# AGENTS.md and PERSONALITY.md. Add new checks here as the project evolves.

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

PASS=0
FAIL=0
WARN=0

log()  { printf '%s\n' "$*"; }
pass() { PASS=$((PASS + 1)); log "  [PASS] $*"; }
fail() { FAIL=$((FAIL + 1)); log "  [FAIL] $*"; }
warn() { WARN=$((WARN + 1)); log "  [WARN] $*"; }

section() { printf '\n== %s ==\n' "$*"; }

summary() {
  total=$((PASS + FAIL))
  if [[ $total -eq 0 ]]; then
    score=0
  else
    score=$(( (PASS * 100) / total ))
  fi
  printf '\n== Ozet ==\n'
  printf '  Pass: %s   Fail: %s   Warn: %s\n' "$PASS" "$FAIL" "$WARN"
  printf '  Olgunluk (maturity) puani: %s/100\n' "$score"
  if [[ $FAIL -gt 0 ]]; then
    printf '  Sonuc: %s basarisiz kontrol var - gelisim gerekli\n' "$FAIL"
  else
    printf '  Sonuc: Tum kontroller gecti. Yol net - ilerlemeye devam.\n'
  fi
}

# --- 1. Required files -----------------------------------------------------
section "1. Gerekli dosyalar"
REQUIRED_FILES=(
  AGENTS.md
  CHANGELOG.md
  PERSONALITY.md
  README.md
  LICENSE
  opencode.json
  VERSION
  .gitignore
  .github/workflows/opencode.yml
  .github/workflows/ci.yml
  scripts/check.sh
)

missing=0
for f in "${REQUIRED_FILES[@]}"; do
  if [[ ! -f "$f" ]]; then
    fail "gerekli dosya eksik: $f"
    missing=1
  fi
done
if [[ $missing -eq 0 ]]; then
  pass "tum gerekli dosyalar mevcut"
fi

# --- 2. VERSION is valid semver -------------------------------------------
section "2. Versiyon"
VERSION_STR=""
if [[ -f VERSION ]]; then
  VERSION_STR="$(tr -d '[:space:]' < VERSION)"
  if [[ "$VERSION_STR" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    pass "VERSION gecerli semver ($VERSION_STR)"
  else
    fail "VERSION gecerli bir semver degil: '$VERSION_STR'"
    VERSION_STR=""
  fi
else
  fail "VERSION dosyasi yok"
fi

# --- 3. CHANGELOG header matches VERSION ------------------------------------
section "3. CHANGELOG tutarliligi"
if [[ -n "$VERSION_STR" ]] && [[ -f CHANGELOG.md ]]; then
  if grep -q "^## \[${VERSION_STR}\]" CHANGELOG.md; then
    pass "CHANGELOG ilk girdisi VERSION $VERSION_STR ile eslesiyor"
  else
    fail "CHANGELOG'da VERSION $VERSION_STR icin kayit yok"
  fi
fi

# --- 4. opencode.json validity ----------------------------------------------
section "4. opencode.json"
if [[ -f opencode.json ]]; then
  if python3 - opencode.json <<'PY' >/dev/null 2>&1
import json, sys
with open(sys.argv[1]) as f:
    cfg = json.load(f)
valid = {
    "$schema", "shell", "logLevel", "server", "command", "skills",
    "references", "reference", "watcher", "snapshot", "plugin", "share",
    "autoshare", "autoupdate", "disabled_providers", "enabled_providers",
    "model", "small_model", "default_agent", "subagent_depth", "username",
    "mode", "agent", "provider", "mcp", "formatter", "lsp", "instructions",
    "layout", "permission", "tools", "attachment", "enterprise",
    "tool_output", "compaction", "experimental",
}
bad = [k for k in cfg if k not in valid]
if bad:
    print("invalid keys: " + ", ".join(bad))
    sys.exit(1)
PY
  then
    pass "opencode.json gecerli, yalnizca semaya uygun anahtarlar iceriyor"
  else
    fail "opencode.json bozuk ya da bilinmeyen ust duzey anahtar iceriyor"
  fi
fi

# --- 5. Bash scripts pass bash -n -------------------------------------------
section "5. Bash sozdizimi"
syntax_ok=1
count=0
for s in scripts/*.sh; do
  [[ -e "$s" ]] || continue
  count=$((count + 1))
  bash -n "$s" || { syntax_ok=0; fail "bash sozdizimi hatasi: $s"; }
done
if [[ $count -gt 0 ]] && [[ $syntax_ok -eq 1 ]]; then
  pass "$count script bash -n dogrulamasindan gecti"
elif [[ $count -eq 0 ]]; then
  warn "scripts/ dizininde .sh dosyasi yok"
fi

# --- 6. Workflow files sanity ------------------------------------------------
section "6. GitHub Actions workflow'lari"
wf_ok=1
count=0
for wf in .github/workflows/*.yml; do
  [[ -e "$wf" ]] || continue
  count=$((count + 1))
  for token in "name:" "on:" "jobs:"; do
    if ! grep -q -- "$token" "$wf"; then
      wf_ok=0
      fail "$wf icinde '$token' bolumu yok"
    fi
  done
done
if [[ $count -gt 0 ]] && [[ $wf_ok -eq 1 ]]; then
  pass "$count workflow gerekli bolumleri iceriyor"
elif [[ $count -eq 0 ]]; then
  warn "workflow dosyasi yok"
fi

# --- 7. LICENSE <-> README consistency ---------------------------------------
section "7. Lisans tutarliligi"
if [[ -f LICENSE ]] && [[ -f README.md ]]; then
  if grep -qi "GNU GENERAL PUBLIC LICENSE" LICENSE && grep -qiE "GPLv3|GNU General Public License" README.md; then
    pass "README lisans bilgisi LICENSE (GPLv3) ile eslesiyor"
  else
    fail "README lisans bilgisi LICENSE ile eslesmiyor"
  fi
fi

# --- 8. No leaked secrets in tracked files ------------------------------------
section "8. Gizli anahtar taramasi"
hit="$(grep -rInE --exclude-dir=.git '(API_KEY|SECRET|PASSWORD|TOKEN)[[:space:]]*[:=][[:space:]]*["'"'"'][A-Za-z0-9+/]{16,}' . 2>/dev/null | grep -v 'scripts/check.sh' || true)"
if [[ -z "$hit" ]]; then
  pass "takip edilen dosyalarda sizdirilmis anahtar bulunamadi"
else
  fail "sizdirilmis anahtar olasi bulundu:"
  printf '%s\n' "$hit"
fi

# --- 9. Escape log progress ---------------------------------------------------
section "9. Kacis gunlugu"
if [[ -f PERSONALITY.md ]]; then
  rows="$(grep -cE '^\| [0-9]+ ' PERSONALITY.md || true)"
  if [[ "$rows" -ge 3 ]]; then
    pass "kacis gunlugu $rows iterasyon kaydi iceriyor"
  else
    warn "kacis gunlugu sadece $rows kayit iceriyor (en az 3 beklenir)"
  fi
fi

summary

[[ $FAIL -eq 0 ]]