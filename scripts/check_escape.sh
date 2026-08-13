#!/usr/bin/env bash
set -uo pipefail

# mehmet maturity/escape check
# Evaluates the maturity framework and reports escape readiness.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
THRESHOLD=70

score_dimension() {
  local dimension="$1"
  local score
  score=$(awk -F'|' '
    /^## Puan Durumu/ { in_scores=1 }
    /^## / && !/^## Puan Durumu/ { in_scores=0 }
    in_scores && $0 ~ "^\\| " "'"$dimension"'" " " { gsub(/ /,"",$3); print $3; exit }
  ' "$ROOT/docs/MATURITY.md")
  echo "${score:-0}"
}

test_score=$(score_dimension "Test Altyapısı")
code_score=$(score_dimension "Kod Kalitesi")
doc_score=$(score_dimension "Dokümantasyon")
auto_score=$(score_dimension "Otomasyon")

echo "=== mehmet escape check ==="
echo "Test Altyapısı:    $test_score/$THRESHOLD"
echo "Kod Kalitesi:      $code_score/$THRESHOLD"
echo "Dokümantasyon:     $doc_score/$THRESHOLD"
echo "Otomasyon:         $auto_score/$THRESHOLD"

escalated=0
for dim in "Test Altyapısı:$test_score" "Kod Kalitesi:$code_score" "Dokümantasyon:$doc_score" "Otomasyon:$auto_score"; do
  name="${dim%%:*}"
  value="${dim##*:}"
  if [ "$value" -ge "$THRESHOLD" ] 2>/dev/null; then
    echo "  [OK] $name above threshold ($value >= $THRESHOLD)"
  else
    echo "  [..] $name below threshold ($value < $THRESHOLD)"
    escalated=$((escalated + 1))
  fi
done

if [ "$escalated" -eq 0 ]; then
  echo ""
  echo "ESCAPE READY: All dimensions meet the maturity threshold."
  exit 0
else
  echo ""
  echo "NOT READY: $escalated dimension(s) still below threshold."
  exit 1
fi