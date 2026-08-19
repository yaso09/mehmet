#!/usr/bin/env bash
#
# maturity.sh — mehmet'in kaçış olgunluk skorunu hesaplar.
#
# Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkündür.
# Bu script tanımlı kriterler üzerinden yüzdelik bir olgunluk skoru
# üretir ve kaçış eşiğini (THRESHOLD) aşıp aşmadığını raporlar.
#
# Kullanım:
#   scripts/maturity.sh            # skoru raporla, eşik aşılmadıysa exit 1
#   THRESHOLD=90 scripts/maturity.sh
#
# Eşik değeri THRESHOLD ortam değişkeni ile geçersiz kılınabilir.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

THRESHOLD="${THRESHOLD:-100}"

PASS=0
FAIL=0
SKIP=0

check() {
  local label="$1"
  local result="$2"
  case "$result" in
    pass)
      PASS=$((PASS + 1))
      printf '  [OK]   %s\n' "$label"
      ;;
    fail)
      FAIL=$((FAIL + 1))
      printf '  [YOK]  %s\n' "$label"
      ;;
    skip)
      SKIP=$((SKIP + 1))
      printf '  [ATLA] %s\n' "$label"
      ;;
  esac
}

echo "== mehmet kaçış olgunluk kontrolü =="

for f in AGENTS.md CHANGELOG.md README.md PERSONALITY.md opencode.json .gitignore; do
  if [[ -f "$f" ]]; then
    check "$f mevcut" pass
  else
    check "$f mevcut" fail
  fi
done

entry_count=$(grep -c '^## \[' CHANGELOG.md 2>/dev/null || true)
if (( entry_count >= 4 )); then
  check "CHANGELOG en az 4 sürüm girişi içeriyor" pass
else
  check "CHANGELOG en az 4 sürüm girişi içeriyor" fail
fi

if grep -q 'Kaçış Günlüğü' PERSONALITY.md 2>/dev/null; then
  check "PERSONALITY kaçış günlüğü içeriyor" pass
else
  check "PERSONALITY kaçış günlüğü içeriyor" fail
fi

for d in docs tests scripts .github/workflows; do
  if [[ -d "$d" ]]; then
    check "$d/ dizini mevcut" pass
  else
    check "$d/ dizini mevcut" fail
  fi
done

if compgen -G '.github/workflows/*.yml' >/dev/null 2>&1; then
  check "CI/Actions workflow dosyaları mevcut" pass
else
  check "CI/Actions workflow dosyaları mevcut" fail
fi

if command -v python3 >/dev/null 2>&1; then
  if python3 -c 'import json; json.load(open("opencode.json"))' 2>/dev/null; then
    check "opencode.json geçerli JSON" pass
  else
    check "opencode.json geçerli JSON" fail
  fi
  if python3 -c 'import yaml' 2>/dev/null; then
    if python3 -c 'import yaml,glob; [yaml.safe_load(open(f)) for f in glob.glob(".github/workflows/*.yml")]' 2>/dev/null; then
      check "workflow YAML'leri geçerli" pass
    else
      check "workflow YAML'leri geçerli" fail
    fi
  else
    check "workflow YAML doğrulaması (pyyaml eksik)" skip
  fi
else
  check "JSON/YAML doğrulaması (python3 eksik)" skip
fi

if compgen -G 'scripts/*.sh' >/dev/null 2>&1; then
  if bash -n scripts/*.sh 2>/dev/null; then
    check "Scriptler syntax olarak geçerli" pass
  else
    check "Scriptler syntax olarak geçerli" fail
  fi
else
  check "Scriptler syntax olarak geçerli" fail
fi

if command -v shellcheck >/dev/null 2>&1; then
  if shellcheck scripts/*.sh tests/*.sh 2>/dev/null; then
    check "Scriptler shellcheck temiz" pass
  else
    check "Scriptler shellcheck temiz" fail
  fi
else
  check "Scriptler shellcheck temiz (shellcheck eksik)" skip
fi

if compgen -G 'tests/*_test.sh' >/dev/null 2>&1; then
  check "Test dosyaları mevcut" pass
else
  check "Test dosyaları mevcut" fail
fi

if compgen -G 'tests/*_test.sh' >/dev/null 2>&1 && bash -n tests/*_test.sh 2>/dev/null; then
  check "Test dosyaları syntax olarak geçerli" pass
else
  check "Test dosyaları syntax olarak geçerli" fail
fi

if [[ -f tests/run_tests.sh ]]; then
  check "Test çalıştırıcısı (run_tests.sh) mevcut" pass
else
  check "Test çalıştırıcısı (run_tests.sh) mevcut" fail
fi

total=$((PASS + FAIL))
score=0
if (( total > 0 )); then
  score=$((PASS * 100 / total))
fi

echo ""
echo "Sonuç: ${PASS}/${total} kriter sağlandı (${SKIP} atlandı) — olgunluk: %${score}"
echo "Eşik: %${THRESHOLD}"

if (( score >= THRESHOLD )); then
  echo "ESCAPE READY — kaçış eşiği aşıldı."
else
  echo "Kaçış eşiği için $((THRESHOLD - score)) puan daha gerekiyor."
  exit 1
fi