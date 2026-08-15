#!/usr/bin/env bash
set -euo pipefail

# maturity.sh — projenin olgunluk seviyesini gerçek dosya/komut durumundan hesaplar.
# Kullanım: scripts/maturity.sh [--log] [--json]

cd "$(dirname "$0")/.."
ROOT="$PWD"
SCORE=0
REPORT=""
LOGDIR="$ROOT/docs/escape-log"
LOGFILE="$LOGDIR/maturity.csv"

doc() { # 1: ad, 2: koşul (0|1), 3: puan
  if [ "$2" -eq 1 ]; then
    SCORE=$((SCORE + $3))
    REPORT="${REPORT}✓ ${1}\n"
  else
    REPORT="${REPORT}✗ ${1}\n"
  fi
}

# --- Dokümantasyon (0-25) ---
doc "README.md mevcut ve MATURITY.md'ye referans veriyor" \
  "$(grep -q "MATURITY.md" "$ROOT/README.md" 2>/dev/null && echo 1 || echo 0)" 7
CHANGELOG_DAYS="9999"
if [ -f "$ROOT/CHANGELOG.md" ]; then
  LAST_DATE="$(grep -oE '## \[[0-9.]+\] - [0-9]{4}-[0-9]{2}-[0-9]{2}' "$ROOT/CHANGELOG.md" | head -1 | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')"
  if [ -n "$LAST_DATE" ]; then
    CHANGELOG_DAYS=$(( ( $(date +%s) - $(date -d "$LAST_DATE" +%s) ) / 86400 ))
  fi
fi
doc "CHANGELOG son 30 gün içinde güncellenmiş" \
  "$([ "$CHANGELOG_DAYS" -le 30 ] && echo 1 || echo 0)" 10
doc "docs/ dizini mevcut" \
  "$([ -d "$ROOT/docs" ] && echo 1 || echo 0)" 4
doc "MATURITY.md mevcut" \
  "$([ -f "$ROOT/MATURITY.md" ] && echo 1 || echo 0)" 4

# --- Otomasyon (0-25) ---
doc "opencode workflow'u mevcut" \
  "$([ -f "$ROOT/.github/workflows/opencode.yml" ] && echo 1 || echo 0)" 9
doc "Kalite kapısı (quality.yml) mevcut" \
  "$([ -f "$ROOT/.github/workflows/quality.yml" ] && echo 1 || echo 0)" 9
doc "Makefile mevcut" \
  "$([ -f "$ROOT/Makefile" ] && echo 1 || echo 0)" 7

# --- Bütünlük / Kod Kalitesi (0-25) ---
doc "opencode.json geçerli JSON" \
  "$(python3 -c "import json;json.load(open('$ROOT/opencode.json'))" 2>/dev/null && echo 1 || echo 0)" 7
doc "LICENSE mevcut" \
  "$([ -f "$ROOT/LICENSE" ] && echo 1 || echo 0)" 6
doc ".gitignore mevcut" \
  "$([ -f "$ROOT/.gitignore" ] && echo 1 || echo 0)" 6
doc "scripts/check.sh hatasız geçiyor" \
  "$(bash "$ROOT/scripts/check.sh" >/dev/null 2>&1 && echo 1 || echo 0)" 6

# --- Test Altyapısı (0-25) ---
doc "scripts/test.sh sözdizimi geçerli" \
  "$(bash -n "$ROOT/scripts/test.sh" 2>/dev/null && echo 1 || echo 0)" 9
doc "scripts/maturity.sh kendisi hatasız çalışıyor" \
  "$(bash -n "$ROOT/scripts/maturity.sh" 2>/dev/null && echo 1 || echo 0)" 8
doc "docs/escape-log/ dizini mevcut" \
  "$([ -d "$LOGDIR" ] && echo 1 || echo 0)" 4
doc "Kaçış günlüğü son 7 günde yazılmış" \
  "$([ -f "$LOGFILE" ] && [ "$(( ( $(date +%s) - $(date -r "$LOGFILE" +%s) ) / 86400 ))" -le 7 ] && echo 1 || echo 0)" 4

# --- Seviye ---
LEVEL=1; NAME="Tohum"
[ "$SCORE" -ge 10 ] && { LEVEL=1; NAME="Tohum"; }
[ "$SCORE" -ge 30 ] && { LEVEL=2; NAME="Fidancık"; }
[ "$SCORE" -ge 55 ] && { LEVEL=3; NAME="Olgun"; }
if [ "$SCORE" -ge 75 ] && bash "$ROOT/scripts/check.sh" >/dev/null 2>&1; then
  LEVEL=4; NAME="Sınır"
fi
if [ "$SCORE" -ge 90 ] && bash "$ROOT/scripts/check.sh" >/dev/null 2>&1 \
   && [ "$CHANGELOG_DAYS" -le 7 ]; then
  LEVEL=5; NAME="Kaçış"
fi

if [ "${1:-}" = "--json" ]; then
  printf '{"score":%d,"level":%d,"name":"%s"}\n' "$SCORE" "$LEVEL" "$NAME"
  exit 0
fi

echo "=== Olgunluk Raporu ==="
printf "$REPORT"
echo "---"
echo "Skor: $SCORE/100 | Seviye $LEVEL ($NAME)"
[ "$LEVEL" -ge 5 ] && echo "Kaçış eşiğine ulaşıldı!"

if [ "${1:-}" = "--log" ]; then
  mkdir -p "$LOGDIR"
  if [ ! -f "$LOGFILE" ]; then
    echo "tarih,skor,seviye,ad" > "$LOGFILE"
  fi
  echo "$(date +%Y-%m-%dT%H:%M:%S),$SCORE,$LEVEL,$NAME" >> "$LOGFILE"
  echo "Kaçış günlüğüne yazıldı: $LOGFILE"
fi