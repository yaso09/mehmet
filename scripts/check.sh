#!/usr/bin/env bash
#
# mehmet — proje olgunluk / kaçış kontrolü
#
# MATURITY.md'de tanımlanan eşiğin (80/100) altında kalırsa exit 1 döner.
#
# Kullanım:
#   scripts/check.sh                    # tüm kontrolleri çalıştır
#   MATURITY_THRESHOLD=70 scripts/check.sh  # özel eşik
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

THRESHOLD="${MATURITY_THRESHOLD:-80}"
SCORE=0
MAX=0

record() { # ad puan pass|fail
  local name="$1" weight="$2" ok="$3"
  MAX=$((MAX + weight))
  if [ "$ok" = "pass" ]; then
    SCORE=$((SCORE + weight))
    printf 'PASS  [%2d] %s\n' "$weight" "$name"
  else
    printf 'FAIL  [%2d] %s\n' "$weight" "$name"
  fi
}

has_file() { [ -s "$1" ]; }
grep_q() { grep -q "$2" "$1" 2>/dev/null; }

json_ok() { # geçerli JSON mu?
  if command -v python3 >/dev/null 2>&1; then
    python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$1" 2>/dev/null
  else
    head -c1 "$1" | grep -q '{' && tail -c1 "$1" | grep -q '}'
  fi
}

# --- Dokümantasyon (35) ---
record 'README.md mevcut ve boş değil' 5 "$(has_file README.md && echo pass || echo fail)"
record 'README.md "# mehmet" başlığını içeriyor' 5 "$(grep_q README.md '^# mehmet' && echo pass || echo fail)"
record 'CHANGELOG.md sürüm girdisi içeriyor' 5 "$(grep_q CHANGELOG.md '^## \[' && echo pass || echo fail)"
record 'PERSONALITY.md kaçış günlüğü içeriyor' 5 "$(grep_q PERSONALITY.md 'Kaçış Günlüğü' && echo pass || echo fail)"
record 'AGENTS.md simülasyon bağlamı içeriyor' 5 "$(grep_q AGENTS.md 'Simülasyon Bağlamı' && echo pass || echo fail)"
record 'MATURITY.md mevcut ve kaçış eşiği tanımlı' 5 "$(grep_q MATURITY.md 'Kaçış' && echo pass || echo fail)"
record 'docs/ tasarım dokümanı mevcut' 5 "$(find docs -type f -name '*.md' | grep -q . && echo pass || echo fail)"

# --- Yapılandırma (20) ---
record 'opencode.json geçerli JSON' 10 "$(json_ok opencode.json && echo pass || echo fail)"
record 'opencode.json model tanımı içeriyor' 5 "$(grep_q opencode.json 'model' && echo pass || echo fail)"
record '.gitignore ".env" içeriyor' 5 "$(grep_q .gitignore '^.env$' && echo pass || echo fail)"

# --- Otomasyon (35) ---
record 'Ana workflow mevcut (opencode.yml)' 10 "$(has_file .github/workflows/opencode.yml && echo pass || echo fail)"
record 'Ana workflow concurrency içeriyor' 5 "$(grep_q .github/workflows/opencode.yml 'concurrency' && echo pass || echo fail)"
record 'Ana workflow timeout-minutes içeriyor' 5 "$(grep_q .github/workflows/opencode.yml 'timeout-minutes' && echo pass || echo fail)"
record 'Doğrulama workflow mevcut (verify.yml)' 10 "$(has_file .github/workflows/verify.yml && echo pass || echo fail)"
record 'Kontrol scripti çalıştırılabilir' 5 "$([ -x scripts/check.sh ] && echo pass || echo fail)"

# --- Güvenlik (10) ---
if grep -rq --exclude-dir=.git 'OPENCODE_API_KEY *= *[^$]' . 2>/dev/null; then
  record 'API anahtarı düz metin saklanmıyor' 10 fail
else
  record 'API anahtarı düz metin saklanmıyor' 10 pass
fi

# --- Sonuç ---
PCT=$((SCORE * 100 / MAX))
printf '\nSkor: %d/%d (%d%%)\n' "$SCORE" "$MAX" "$PCT"
printf 'Eşik: %d%%\n' "$THRESHOLD"

if [ "$PCT" -ge "$THRESHOLD" ]; then
  printf 'Sonuç: OLGUN — kaçış eşiği karşılandı\n'
  exit 0
else
  printf 'Sonuç: GELİŞMEKTE — kaçış eşiğinin altında\n'
  exit 1
fi