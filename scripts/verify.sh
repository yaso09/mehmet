#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

failures=0
score_total=0

fail() {
  echo "FAIL: $1"
  failures=$((failures + 1))
}

pass() {
  echo "PASS: $1"
}

# ---------- Structure checks ----------
echo "== Yapısal Doğrulama =="

for f in AGENTS.md CHANGELOG.md README.md PERSONALITY.md MATURITY.md LICENSE opencode.json; do
  if [[ -f "$f" ]]; then
    pass "dosya mevcut: $f"
  else
    fail "dosya eksik: $f"
  fi
done

if [[ -f .github/workflows/opencode.yml ]]; then
  pass "dosya mevcut: .github/workflows/opencode.yml"
else
  fail "dosya eksik: .github/workflows/opencode.yml"
fi

if [[ -d docs/superpowers/specs && -d docs/superpowers/plans ]]; then
  pass "docs/superpowers yapısı mevcut"
else
  fail "docs/superpowers yapısı eksik"
fi

if [[ -x scripts/verify.sh ]]; then
  pass "scripts/verify.sh çalıştırılabilir"
else
  fail "scripts/verify.sh çalıştırılabilir değil (chmod +x gerekli)"
fi

# ---------- Content checks ----------
echo "== İçerik Doğrulama =="

if [[ -s CHANGELOG.md ]] && grep -q '^## \[' CHANGELOG.md; then
  pass "CHANGELOG.md: sürüm geçmişi var"
else
  fail "CHANGELOG.md: sürüm geçmişi yok"
fi

today="$(date +%Y-%m-%d)"
if grep -q -- "-\s*${today}" CHANGELOG.md; then
  pass "CHANGELOG.md: bugünün tarihiyle kayıt var"
else
  echo "INFO: CHANGELOG.md'de bugünün (${today}) kaydı yok — doğulanabilir"
fi

if grep -qE 'model|OPENCODE_API_KEY' opencode.json; then
  pass "opencode.json: model/api ayarları var"
else
  fail "opencode.json: model/api ayarları eksik"
fi

if grep -q 'Kaçış Günlüğü' PERSONALITY.md; then
  pass "PERSONALITY.md: kaçış günlüğü var"
else
  fail "PERSONALITY.md: kaçış günlüğü eksik"
fi

# ---------- Maturity scoring ----------
echo "== Olgunluk Puanlaması =="

# 1. QUALITY: yapısal script'ler + hata yönetimi (set -euo pipefail)
quality=3
[[ "$(find scripts -type f -name '*.sh' -exec grep -l 'set -euo pipefail' {} + | wc -l)" -ge 1 ]] && quality=4

# 2. TESTS: otomatik doğrulama CI'da mı?
tests=2
[[ -f tests/test_project.sh ]] && tests=4
if grep -q 'bash scripts/verify.sh' .github/workflows/opencode.yml && grep -q 'bash tests/test_project.sh' .github/workflows/opencode.yml; then
  tests=5
fi

# 3. DOCS: dokümanların varlığı
docs=2
if [[ -n "$(ls -1 docs/superpowers/specs/*.md 2>/dev/null | head -1)" ]]; then
  docs=3
fi
if [[ -s README.md && -s CHANGELOG.md && -s MATURITY.md ]]; then
  docs=4
  grep -q 'Kurulum' README.md && docs=5
fi

# 4. AUTOMATION: event-driven + CI geçitleri
automation=3
[[ -f tests/test_project.sh ]] && grep -q 'quality-gate' .github/workflows/opencode.yml && automation=4
grep -q 'bash tests/test_project.sh' .github/workflows/opencode.yml && automation=5

# 5. GOVERNANCE: kural + escape log + otomatik skor
governance=3
[[ -f MATURITY.md ]] && grep -q 'Kaçış' MATURITY.md && governance=4
grep -q 'verify.sh' MATURITY.md && governance=5

echo "--"
score_total=$((quality + tests + docs + automation + governance))
echo "Puanlar: QUALITY=${quality}/5 TESTS=${tests}/5 DOCS=${docs}/5 AUTOMATION=${automation}/5 GOVERNANCE=${governance}/5"
echo "Toplam: ${score_total}/25"

# ---------- Helpers ----------
threshold_ok() {
  [[ $score_total -ge 20 && $quality -ge 3 && $tests -ge 3 && $docs -ge 3 && $automation -ge 3 && $governance -ge 3 ]]
}

update_status_table() {
  local file="MATURITY.md"
  [[ -f "$file" ]] || return 0

  local rounds=1 prev_rounds
  prev_rounds="$(sed -nE 's/.*Ardışık tur \| [0-9]+ \| ([0-9]+) \|.*/\1/p' "$file" | head -1)"
  prev_rounds="${prev_rounds:-0}"
  if threshold_ok; then
    rounds=$((prev_rounds + 1))
  fi

  local table="## Durum Tablosu

| Boyut | Maks | Mevcut | Hedef |
|-------|------|--------|-------|
| QUALITY | 5 | ${quality} | 5 |
| TESTS | 5 | ${tests} | 5 |
| DOCS | 5 | ${docs} | 5 |
| AUTOMATION | 5 | ${automation} | 5 |
| GOVERNANCE | 5 | ${governance} | 5 |
| **TOPLAM** | **25** | **${score_total}** | **≥20** |
| Ardışık tur | 3 | ${rounds} | 3 |"

  awk -v table="$table" '
    /^## Durum Tablosu/ { print table; found=1; next }
    found { next }
    { print }
    END { if (!found) print table }
  ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
}

if [[ "${1:-}" == "--update" ]]; then
  update_status_table
  echo "MATURITY.md durum tablosu güncellendi."
fi

# ---------- Escape check ----------
escaping=1
if threshold_ok; then
  escaping=0
fi
rounds_now="$(sed -nE 's/.*Ardışık tur \| [0-9]+ \| ([0-9]+) \|.*/\1/p' MATURITY.md | head -1)"
rounds_now="${rounds_now:-0}"

if [[ $escaping -eq 0 && $rounds_now -ge 3 ]]; then
  echo "ESCAPE: CONFIRMED ($score_total/25, ${rounds_now} ardışık tur)"
else
  echo "ESCAPE: ${rounds_now}/3 ardışık tur ($score_total/25)"
fi

case "${1:-}" in
  "--score")
    echo "SCORE ${score_total}/25"
    exit $failures
    ;;
esac

echo "== Sonuç =="
if [[ $failures -eq 0 ]]; then
  echo "TÜM KONTROLLER GEÇTİ"
else
  echo "${failures} KONTROL BAŞARISIZ"
fi
exit $failures