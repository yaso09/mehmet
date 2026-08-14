#!/usr/bin/env bash
#
# maturity.sh — mehmet olgunluk skoru hesaplayıcı.
#
# docs/maturity.json içindeki boyut puanlarını ve ağırlıkları okur,
# ağırlıklı ortalamayı (0–100) hesaplar ve kaçış eşiğini kontrol eder.
#
# Çıkış:
#   0 — kaçış koşulu sağlandı
#   1 — kaçış koşulu sağlanmadı
#
# Kullanım:
#   ./scripts/maturity.sh

set -euo pipefail

cd "$(dirname "$0")/.."

DATA="docs/maturity.json"

if [[ ! -f "$DATA" ]]; then
  echo "[FAIL] $DATA bulunamadı" >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "[FAIL] python3 gerekli" >&2
  exit 1
fi

OUTPUT="$(python3 - "$DATA" <<'PY'
import json, sys, math

with open(sys.argv[1]) as f:
    data = json.load(f)

weights = data["weights"]
scores = data["scores"]

total_weight = sum(weights.values())
if total_weight == 0:
    raise SystemExit("toplam ağırlık 0 olamaz")

weighted = sum(scores[k] * weights[k] for k in weights)
score = round(weighted / total_weight * 100 / 5, 1)

escape = data["escape"]
min_total = escape["min_total"]
min_test = escape["min_test"]

print(json.dumps({
    "score": score,
    "total_weight": total_weight,
    "min_total": min_total,
    "min_test": min_test,
    "test_score": scores.get("test", 0),
    "escape": score >= min_total and scores.get("test", 0) >= min_test,
}))
PY
)"

SCORE="$(echo "$OUTPUT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["score"])')"
ESCAPE="$(echo "$OUTPUT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["escape"])')"
MIN_TOTAL="$(echo "$OUTPUT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["min_total"])')"
MIN_TEST="$(echo "$OUTPUT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["min_test"])')"
TEST_SCORE="$(echo "$OUTPUT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["test_score"])')"

echo "Olgunluk skoru: $SCORE / 100"
echo "Kaçış eşiği: toplam >= $MIN_TOTAL VE test boyutu >= $MIN_TEST"
echo "Mevcut test boyutu: $TEST_SCORE"

if [[ "$ESCAPE" == "True" ]]; then
  echo "SONUÇ: Kaçış koşulu SAĞLANDI."
  exit 0
else
  echo "SONUÇ: Kaçış koşulu sağlanmadı."
  exit 1
fi