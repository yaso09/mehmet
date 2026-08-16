#!/usr/bin/env bash
set -uo pipefail

# mehmet — olgunluk ölçüm scripti
# Projenin olgunluk seviyesini 12 kriter üzerinden skorlar ve kaçış eşiğini denetler.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MAX_SCORE=12
ESCAPE_THRESHOLD="${ESCAPE_THRESHOLD:-11}"

score=0
declare -a passed=()
declare -a failed=()

check() {
  local name="$1"
  local ok="$2"
  if [[ "$ok" == "true" ]]; then
    score=$((score + 1))
    passed+=("$name")
  else
    failed+=("$name")
  fi
}

file_non_empty() {
  if [[ -s "$ROOT/$1" ]]; then echo true; else echo false; fi
}

# --- 1. Temel dosyalar ---
check "AGENTS.md mevcut ve dolu" "$(file_non_empty AGENTS.md)"
check "CHANGELOG.md mevcut ve dolu" "$(file_non_empty CHANGELOG.md)"
check "README.md mevcut ve dolu" "$([[ -s "$ROOT/README.md" ]] && (( $(wc -c < "$ROOT/README.md") > 100 )) && echo true || echo false)"
check "PERSONALITY.md mevcut ve dolu" "$(file_non_empty PERSONALITY.md)"
check "LICENSE mevcut" "$(file_non_empty LICENSE)"
check ".gitignore mevcut" "$(file_non_empty .gitignore)"

# --- 2. Konfigürasyon ---
check "opencode.json geçerli JSON" "$(command -v python3 >/dev/null 2>&1 && python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$ROOT/opencode.json" 2>/dev/null && echo true || echo false)"
check "Workflow dosyası mevcut ve validate job'u var" "$([[ -f "$ROOT/.github/workflows/opencode.yml" ]] && grep -q 'validate:' "$ROOT/.github/workflows/opencode.yml" && echo true || echo false)"

# --- 3. Dokümantasyon ---
check "docs/ klasörü dolu" "$([[ -n "$(find "$ROOT/docs" -type f 2>/dev/null)" ]] && echo true || echo false)"
check "MATURITY.md mevcut ve dolu" "$(file_non_empty MATURITY.md)"

# --- 4. Kalite ---
check "Test altyapısı mevcut" "$(file_non_empty tests/integrity_test.sh)"
check "Testler başarılı" "$(bash "$ROOT/tests/integrity_test.sh" >/dev/null 2>&1 && echo true || echo false)"

# --- Çıktı ---
echo "=== mehmet olgunluk skoru: $score/$MAX_SCORE ==="
if [[ ${#passed[@]} -gt 0 ]]; then
  echo "GEÇTİ:"
  printf '  - %s\n' "${passed[@]}"
fi
if [[ ${#failed[@]} -gt 0 ]]; then
  echo "KALDI:"
  printf '  - %s\n' "${failed[@]}"
fi

if [[ "${1:-}" == "--check" ]]; then
  if (( score >= ESCAPE_THRESHOLD )); then
    echo "Kaçış eşiği aşıldı (eşik: $ESCAPE_THRESHOLD). Olgunluk seviyesi yeterli."
    exit 0
  else
    echo "Kaçış eşiğine ulaşılamadı (eşik: $ESCAPE_THRESHOLD). Eksik kriterler var."
    exit 1
  fi
fi

exit 0