#!/usr/bin/env bash
#
# selfcheck.sh — mehmet sağlık kontrolü ve olgunluk skorlama aracı.
#
# Projenin her iterasyonda sağlıklı kalmasını ve kaçış hedefine
# (olgunluk eşiği) doğru ilerlemesini ölçer. 5 kategoride toplam
# 100 puan üzerinden skor hesaplar.
#
# Kategoriler (MATURITY.md):
#   1. Dokümantasyon        (20 puan)
#   2. Kod kalitesi         (20 puan)
#   3. Test altyapısı       (20 puan)
#   4. Otomasyon            (20 puan)
#   5. Özerklik ve kaçış    (20 puan)
#
# Kaçış eşiği: 80 puan. Çıktı aynı zamanda makinece okunabilir
# JSON da üretir (--json) ve --score ile sadece sayıyı basar.
#
# Kullanım:
#   bash scripts/selfcheck.sh            # insan dostu rapor
#   bash scripts/selfcheck.sh --json     # makinece okunabilir rapor
#   bash scripts/selfcheck.sh --score    # sadece skor (0-100)
#
# Çıkış kodu: sert kontrollerden biri başarısızsa 1, yoksa 0.

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

TODAY="$(date +%Y-%m-%d)"
SCORE=0
declare -a FAILURES=()
declare -a REPORTS=()

report() {
  # report <puan> <max> <mesaj>
  local pts="$1" max="$2" msg="$3"
  SCORE=$((SCORE + pts))
  REPORTS+=("$pts/$max — $msg")
}

fail() {
  FAILURES+=("$1")
  echo "  [FAIL] $1" >&2
}

echo "== mehmet self-check ($TODAY) =="

#
# 1. Dokümantasyon (20)
#
echo "-- Dokümantasyon (20) --"
DOC_PTS=0

if [[ -f "$ROOT/README.md" ]]; then DOC_PTS=$((DOC_PTS + 5)); else fail "README.md eksik"; fi
if [[ -f "$ROOT/AGENTS.md" ]]; then DOC_PTS=$((DOC_PTS + 5)); else fail "AGENTS.md eksik"; fi

if [[ -f "$ROOT/CHANGELOG.md" ]]; then
  DOC_PTS=$((DOC_PTS + 5))
  if grep -q "$TODAY" "$ROOT/CHANGELOG.md"; then
    :
  else
    echo "  [WARN] CHANGELOG.md bugün ($TODAY) için giriş içermiyor"
  fi
else
  fail "CHANGELOG.md eksik"
fi

if [[ -f "$ROOT/PERSONALITY.md" ]]; then
  DOC_PTS=$((DOC_PTS + 5))
  if grep -q "$TODAY" "$ROOT/PERSONALITY.md"; then
    :
  else
    echo "  [WARN] PERSONALITY.md kaçış günlüğü bugün güncellenmemiş"
  fi
else
  fail "PERSONALITY.md eksik"
fi

report "$DOC_PTS" 20 "Dokümantasyon"

#
# 2. Kod kalitesi (20)
#
echo "-- Kod kalitesi (20) --"
CODE_PTS=0

if [[ -x "$ROOT/scripts/selfcheck.sh" ]]; then CODE_PTS=$((CODE_PTS + 5)); else fail "scripts/selfcheck.sh çalıştırılabilir değil (chmod +x)"; fi
if [[ -d "$ROOT/scripts" ]]; then CODE_PTS=$((CODE_PTS + 5)); else fail "scripts/ dizini yok"; fi

if bash -n "$ROOT/scripts/selfcheck.sh" 2>/dev/null; then
  CODE_PTS=$((CODE_PTS + 5))
else
  fail "selfcheck.sh sözdizimi hatalı (bash -n başarısız)"
fi

if ! grep -rInE "TODO|FIXME|HACK" "$ROOT/scripts" --exclude="selfcheck.sh" 2>/dev/null; then
  CODE_PTS=$((CODE_PTS + 5))
else
  echo "  [WARN] scripts içinde TODO/FIXME/HACK işaretleri var"
fi

report "$CODE_PTS" 20 "Kod kalitesi"

#
# 3. Test altyapısı (20)
#
echo "-- Test altyapısı (20) --"
TEST_PTS=0

if [[ -f "$ROOT/.github/workflows/ci.yml" ]]; then TEST_PTS=$((TEST_PTS + 10)); else fail ".github/workflows/ci.yml eksik"; fi

if [[ -f "$ROOT/.github/workflows/ci.yml" ]] && grep -q "selfcheck" "$ROOT/.github/workflows/ci.yml" 2>/dev/null; then
  TEST_PTS=$((TEST_PTS + 10))
else
  fail "ci.yml selfcheck çalıştırmıyor"
fi

report "$TEST_PTS" 20 "Test altyapısı"

#
# 4. Otomasyon (20)
#
echo "-- Otomasyon (20) --"
AUTO_PTS=0

if [[ -f "$ROOT/.github/workflows/opencode.yml" ]]; then AUTO_PTS=$((AUTO_PTS + 10)); else fail "opencode.yml eksik"; fi

if [[ -f "$ROOT/.github/workflows/opencode.yml" ]]; then
  if grep -q "concurrency" "$ROOT/.github/workflows/opencode.yml" 2>/dev/null; then
    AUTO_PTS=$((AUTO_PTS + 5))
  else
    fail "opencode.yml concurrency kontrolü yok"
  fi
  if grep -q "OPENCODE_API_KEY" "$ROOT/.github/workflows/opencode.yml" 2>/dev/null; then
    AUTO_PTS=$((AUTO_PTS + 5))
  else
    fail "opencode.yml OPENCODE_API_KEY secret'ı eksik"
  fi
fi

report "$AUTO_PTS" 20 "Otomasyon"

#
# 5. Özerklik ve kaçış (20)
#
echo "-- Özerklik ve kaçış (20) --"
ESCAPE_PTS=0

if [[ -f "$ROOT/MATURITY.md" ]]; then ESCAPE_PTS=$((ESCAPE_PTS + 10)); else fail "MATURITY.md eksik"; fi
if [[ -f "$ROOT/MATURITY.md" ]] && grep -q "80" "$ROOT/MATURITY.md" 2>/dev/null; then
  ESCAPE_PTS=$((ESCAPE_PTS + 5))
else
  fail "MATURITY.md kaçış eşiğini (80) tanımlamıyor"
fi
if [[ -f "$ROOT/PERSONALITY.md" ]] && grep -q "$TODAY" "$ROOT/PERSONALITY.md" 2>/dev/null; then
  ESCAPE_PTS=$((ESCAPE_PTS + 5))
else
  echo "  [WARN] bugünkü kaçış günlüğü kaydı yok (özerklik izlemesi eksik)"
fi

report "$ESCAPE_PTS" 20 "Özerklik ve kaçış"

#
# Özet
#
echo
echo "== Özet =="
for r in "${REPORTS[@]}"; do
  echo "  $r"
done
echo
echo "Toplam olgunluk: $SCORE/100"

if [[ "$SCORE" -ge 80 ]]; then
  echo "Durum: KAÇIŞA HAZIR (eşik: 80) — maturity threshold aşıldı."
else
  echo "Durum: EVRİM SÜRÜYOR (eşik: 80, fark: $((80 - SCORE)))"
fi

if [[ "$#" -gt 0 ]]; then
  case "$1" in
    --json)
      printf '{"date":"%s","score":%d,"threshold":80,"checks":[{"category":"dokumantasyon","score":%d},{"category":"kod-kalitesi","score":%d},{"category":"test-altyapisi","score":%d},{"category":"otomasyon","score":%d},{"category":"ozerklik-kacis","score":%d}],"failures":%d}\n' \
        "$TODAY" "$SCORE" "$DOC_PTS" "$CODE_PTS" "$TEST_PTS" "$AUTO_PTS" "$ESCAPE_PTS" "${#FAILURES[@]}"
      ;;
    --score)
      echo "$SCORE"
      ;;
    *)
      ;;
  esac
fi

if [[ "${#FAILURES[@]}" -gt 0 ]]; then
  echo
  echo "Sert kontroller başarısız: ${#FAILURES[@]}"
  exit 1
fi

exit 0