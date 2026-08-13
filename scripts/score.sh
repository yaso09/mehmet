#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "== Olgunluk Skoru =="

LATEST="$(grep -E '^\| [0-9]{4}-' MATURITY.md | tail -1)"
echo "$LATEST"

TOTAL="$(echo "$LATEST" | awk -F'|' '{gsub(/ /,"",$7); print $7}')"
THRESHOLD=80

if [[ -n "$TOTAL" ]] && [[ "$TOTAL" =~ ^[0-9]+$ ]]; then
  if [[ "$TOTAL" -ge "$THRESHOLD" ]]; then
    echo "Durum: EŞİK AŞILDI (>= $THRESHOLD) — kaçış mekanizması adayı"
    exit 0
  else
    echo "Durum: Eşiğin altında (< $THRESHOLD) — gelişmeye devam"
    exit 1
  fi
else
  echo "Uyarı: Skor çözümlenemedi, son satırı kontrol edin."
  exit 1
fi
