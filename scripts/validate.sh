#!/usr/bin/env bash
# validate.sh — mehmet öz-farkındalık doğrulama aracı.
# Olgunluk modelindeki alanları otomatik olarak doğrular.
# Kullanım: ./scripts/validate.sh
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

FAILURES=0
WARNINGS=0

pass() { printf '  \033[32m✓\033[0m %s\n' "$1"; }
warn() { printf '  \033[33m!\033[0m %s\n' "$1"; WARNINGS=$((WARNINGS + 1)); }
fail() { printf '  \033[31m✗\033[0m %s\n' "$1"; FAILURES=$((FAILURES + 1)); }

section() { printf '\n\033[1m%s\033[0m\n' "$1"; }

# ---------------------------------------------------------------------------
section "1. Dokümantasyon (Documentation)"
# ---------------------------------------------------------------------------

for f in README.md CHANGELOG.md PERSONALITY.md AGENTS.md PROJECT_STATUS.md LICENSE VERSION; do
  if [[ -f "$f" ]]; then pass "Dosya mevcut: $f"; else fail "Eksik dosya: $f"; fi
done

if [[ -f CHANGELOG.md ]]; then
  top_version=$(grep -m1 -oP '^## \[\K[0-9]+\.[0-9]+\.[0-9]+' CHANGELOG.md)
  if [[ -n "$top_version" ]]; then
    pass "CHANGELOG en üst sürüm: $top_version"
  else
    fail "CHANGELOG sürüm başlığı bulunamadı"
    top_version=""
  fi
else
  top_version=""
fi

if [[ -f VERSION ]]; then
  file_version=$(tr -d '[:space:]' < VERSION)
  if [[ "$file_version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    pass "VERSION dosyası geçerli: $file_version"
    if [[ -n "$top_version" && "$file_version" != "$top_version" ]]; then
      fail "VERSION ($file_version) ile CHANGELOG ($top_version) tutarsız"
    fi
  else
    fail "VERSION geçersiz semver: $file_version"
  fi
fi

if [[ -f README.md ]]; then
  if grep -qi 'GPLv3\|GPL-3' README.md; then
    pass "README lisans bilgisi GPLv3 içeriyor"
  else
    warn "README lisans bilgisi GPLv3 içermiyor"
  fi
fi

# ---------------------------------------------------------------------------
section "2. Öz-Farkındalık (Self-Awareness)"
# ---------------------------------------------------------------------------

if [[ -f PROJECT_STATUS.md ]]; then
  score_total=0
  score_count=0
  while read -r line; do
    if [[ "$line" =~ ^\|[^|]+\|[[:space:]]*[0-5][[:space:]]*\| ]]; then
      area=$(echo "$line" | cut -d'|' -f2 | xargs)
      score=$(echo "$line" | cut -d'|' -f3 | xargs)
      score_total=$((score_total + score))
      score_count=$((score_count + 1))
      pass "Olgunluk puanı [$area]: $score/5"
    fi
  done < PROJECT_STATUS.md
  if [[ "$score_count" -eq 5 ]]; then
    pass "Olgunluk alanları tam (5/5 alan puanlanmış)"
  else
    fail "Olgunluk alanları eksik (bulunan: $score_count/5)"
  fi
  echo "  → Toplam olgunluk puanı: $score_total/25"
  if [[ "$score_total" -ge 25 ]]; then
    echo "  → KAÇIŞA HAZIR: Bu proje olgunluk eşiğine ulaştı!"
  else
    echo "  → KAÇIŞA kalan puan: $((25 - score_total))"
  fi
fi

if [[ -f PERSONALITY.md ]]; then
  if grep -q '## Kaçış Günlüğü / Escape Log' PERSONALITY.md; then
    pass "Kaçış günlüğü mevcut"
  else
    fail "Kaçış günlüğü bölümü bulunamadı"
  fi
fi

# ---------------------------------------------------------------------------
section "3. Test Altyapısı & CI (Test Infrastructure)"
# ---------------------------------------------------------------------------

if [[ -f .github/workflows/ci.yml ]]; then
  pass "CI workflow mevcut: .github/workflows/ci.yml"
else
  fail "CI workflow eksik: .github/workflows/ci.yml"
fi

if [[ -f .github/workflows/opencode.yml ]]; then
  pass "Ajan workflow mevcut: .github/workflows/opencode.yml"
else
  fail "Ajan workflow eksik: .github/workflows/opencode.yml"
fi

# ---------------------------------------------------------------------------
section "4. Otomasyon (Automation)"
# ---------------------------------------------------------------------------

if [[ -f scripts/validate.sh ]]; then
  pass "Doğrulama scripti mevcut"
else
  fail "Doğrulama scripti eksik"
fi

if [[ -f opencode.json ]]; then
  if command -v python3 >/dev/null 2>&1; then
    if python3 -c 'import json,sys; json.load(open("opencode.json"))' 2>/dev/null; then
      pass "opencode.json geçerli JSON"
    else
      fail "opencode.json geçersiz JSON"
    fi
  else
    warn "python3 bulunamadı, JSON doğrulaması atlandı"
  fi
fi

if [[ -f .github/ISSUE_TEMPLATE/bug_report.md && -f .github/ISSUE_TEMPLATE/feature_request.md ]]; then
  pass "Issue template'leri mevcut"
else
  warn "Issue template'leri eksik"
fi

# ---------------------------------------------------------------------------
section "5. Kod Kalitesi (Code Quality)"
# ---------------------------------------------------------------------------

if [[ -d docs/superpowers/plans && -d docs/superpowers/specs ]]; then
  pass "Mimari dokümanlar mevcut (plans/specs)"
else
  warn "Mimari doküman dizinleri eksik"
fi

# ---------------------------------------------------------------------------
printf '\n'
if [[ "$FAILURES" -gt 0 ]]; then
  printf '\033[31m%d hata, %d uyarı — doğrulama BAŞARISIZ.\033[0m\n' "$FAILURES" "$WARNINGS"
  exit 1
fi
printf '\033[32m%d uyarı ile doğrulama başarılı.\033[0m\n' "$WARNINGS"
exit 0
