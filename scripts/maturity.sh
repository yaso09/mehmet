#!/usr/bin/env bash
# mehmet olgunluk (maturity) değerlendiricisi
# Kaçış hedefi için ölçülebilir ilerleme skoru üretir: 0-100.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
score=0
report=()

# --- Kategori 1: Temel dosyalar (15) ---
core=0
for f in AGENTS.md CHANGELOG.md PERSONALITY.md README.md opencode.json LICENSE; do
  [[ -f "$ROOT/$f" ]] && core=$((core + 1))
done
core=$((core * 15 / 6))
score=$((score + core))
report+=("CORE  temel dosyalar $core/15")

# --- Kategori 2: Dokümantasyon (15) ---
docs=0
[[ -d "$ROOT/docs" ]] && docs=$((docs + 4))
grep -q '^## ' "$ROOT/README.md" && docs=$((docs + 4))
[[ $(grep -c '^## \[' "$ROOT/CHANGELOG.md" 2>/dev/null || echo 0) -ge 3 ]] && docs=$((docs + 4))
[[ -f "$ROOT/LICENSE" ]] && docs=$((docs + 3))
score=$((score + docs))
report+=("DOCS  dokümantasyon kalitesi $docs/15")

# --- Kategori 3: Doğrulama (20) ---
if [[ -f "$ROOT/scripts/validate.sh" ]] && bash "$ROOT/scripts/validate.sh" >/dev/null 2>&1; then
  validation=20
else
  validation=0
fi
score=$((score + validation))
report+=("VAL   bütünlük doğrulaması $validation/20")

# --- Kategori 4: Test altyapısı (20) ---
testing=0
if [[ -x "$ROOT/tests/run_tests.sh" ]]; then
  testing=5
  if [[ "${MEHMET_RECURSION_GUARD:-}" != "1" ]] && MEHMET_RECURSION_GUARD=1 bash "$ROOT/tests/run_tests.sh" >/dev/null 2>&1; then
    testing=20
  fi
fi
score=$((score + testing))
report+=("TEST  test altyapısı $testing/20")

# --- Kategori 5: Otomasyon (15) ---
auto=0
[[ -f "$ROOT/.github/workflows/opencode.yml" ]] && auto=$((auto + 5))
grep -q "concurrency" "$ROOT/.github/workflows/opencode.yml" && auto=$((auto + 3))
[[ -f "$ROOT/.github/workflows/validate.yml" ]] && auto=$((auto + 4))
[[ -f "$ROOT/Makefile" ]] && auto=$((auto + 3))
score=$((score + auto))
report+=("AUTO  CI otomasyonu $auto/15")

# --- Kategori 6: Release / Topluluk cilası (15) ---
release=0
[[ -d "$ROOT/.github/ISSUE_TEMPLATE" ]] && release=$((release + 4))
[[ -f "$ROOT/.github/PULL_REQUEST_TEMPLATE.md" ]] && release=$((release + 4))
[[ -f "$ROOT/.github/workflows/release.yml" ]] && release=$((release + 4))
[[ -f "$ROOT/CONTRIBUTING.md" ]] && release=$((release + 3))
score=$((score + release))
report+=("RELS  release/topluluk cilası $release/15")

echo "MEHMET MATURITY SCORE: $score/100"
echo ""
printf '%s\n' "${report[@]}"

if   [[ $score -ge 90 ]]; then level="ESCAPE READY"
elif [[ $score -ge 70 ]]; then level="Autonomous"
elif [[ $score -ge 50 ]]; then level="Self-Improving"
elif [[ $score -ge 30 ]]; then level="Aware"
else level="Nascent"
fi
echo ""
echo "LEVEL: $level"
