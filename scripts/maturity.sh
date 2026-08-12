#!/usr/bin/env bash
#
# maturity.sh - mehmet olgunluk ölçüm motoru
#
# Kullanım:
#   scripts/maturity.sh            → insan okunur rapor
#   scripts/maturity.sh --report   → aynı (varsayılan)
#   scripts/maturity.sh --score    → sadece sayı (0-100)
#   scripts/maturity.sh --json     → JSON çıktısı (stdout)
#   scripts/maturity.sh --record   → docs/measures.json güncelle
#   scripts/maturity.sh --verify   → CI için: hata varsa exit 1
#   scripts/maturity.sh --test     → kendi kendini test et
#
# Kaçış eşiği: skor >= ESCAPE_SCORE, ardışık ESCAPE_STREAK iterasyon boyunca.

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PTS=5
TOTAL_CHECKS=20
ESCAPE_SCORE="${ESCAPE_SCORE:-90}"
ESCAPE_STREAK="${ESCAPE_STREAK:-3}"

C_OK="\033[32m"; C_FAIL="\033[31m"; C_WARN="\033[33m"; C_END="\033[0m"

PASS=0
FAIL=0
SCORE=0
declare -a RESULT

pass() { PASS=$((PASS + 1)); RESULT+=("ok: $1"); }
fail() { FAIL=$((FAIL + 1)); RESULT+=("fail: $1"); }

has_file() { if [[ -f "$1" ]]; then pass "$2"; else fail "$2"; fi; }
has_dir()  { if [[ -d "$1" ]]; then pass "$2"; else fail "$2"; fi; }
has_text() { if grep -q "$1" "$2" 2>/dev/null; then pass "$3"; else fail "$3"; fi; }

changelog_version() {
  sed -n 's/^## \[\([0-9.]*\)\].*/\1/p' CHANGELOG.md 2>/dev/null | head -n1
}

json_field() {
  node -e '
    const fs=require("fs");
    try {
      const d=JSON.parse(fs.readFileSync(process.argv[1],"utf8"));
      const p=process.argv[2];
      let v=d;
      for (const k of p.split(".")) v = (v==null?null:v[k]);
      console.log(v==null?"":v);
    } catch(e){ console.log(""); }
  ' "$1" "$2" 2>/dev/null
}

run_checks() {
  # --- Dokümantasyon & Yönetim (7) ---
  has_file "README.md" "README.md mevcut"
  has_file "CHANGELOG.md" "CHANGELOG.md mevcut"
  has_file "PERSONALITY.md" "PERSONALITY.md mevcut"
  has_file "MATURITY.md" "MATURITY.md mevcut"
  has_file "LICENSE" "LICENSE mevcut"
  has_file ".gitignore" ".gitignore mevcut"
  if [[ -n "$(changelog_version)" ]] && grep -Eq '^## \[[0-9.]+\]' CHANGELOG.md; then
    pass "CHANGELOG sürüm kaydı var"
  else
    fail "CHANGELOG sürüm kaydı var"
  fi

  # --- Konfigürasyon & Kod (6) ---
  if [[ -f "opencode.json" ]] && node -e 'JSON.parse(require("fs").readFileSync("opencode.json","utf8"))' 2>/dev/null; then
    pass "opencode.json geçerli JSON"
  else
    fail "opencode.json geçerli JSON"
  fi
  has_text '"model"' "opencode.json" "opencode.json model tanımlı"
  has_file ".github/workflows/opencode.yml" "Workflow dosyası mevcut"
  has_text "concurrency" ".github/workflows/opencode.yml" "Workflow concurrency koruması var"
  has_text "permissions:" ".github/workflows/opencode.yml" "Workflow scoped permissions var"
  has_text "schedule" ".github/workflows/opencode.yml" "Workflow schedule trigger var"

  # --- Dokümantasyon & Planlar (3) ---
  has_dir "docs/superpowers/specs" "Tasarım spec (specs) mevcut"
  has_dir "docs/superpowers/plans" "Uygulama planı (plans) mevcut"
  if grep -qi "olgunluk\|maturit" "README.md" 2>/dev/null; then
    pass "README olgunluk (maturity) bilgisi içeriyor"
  else
    fail "README olgunluk (maturity) bilgisi içeriyor"
  fi

  # --- Otomasyon & Testler (4) ---
  if [[ -f "scripts/maturity.sh" && -x "scripts/maturity.sh" ]]; then
    pass "maturity.sh mevcut ve çalıştırılabilir"
  else
    fail "maturity.sh mevcut ve çalıştırılabilir"
  fi
  has_file "docs/measures.json" "Ölçüm raporu (measures.json) mevcut"
  has_text "verify" ".github/workflows/opencode.yml" "CI verify job mevcut"
  local rows
  rows="$(grep -cE '^\| *[0-9]+ *\|' PERSONALITY.md 2>/dev/null || true)"
  if [[ "$rows" -ge 3 ]]; then
    pass "Kaçış günlüğünde en az 3 iterasyon kaydı var"
  else
    fail "Kaçış günlüğünde en az 3 iterasyon kaydı var"
  fi
}

render() {
  SCORE=$((PASS * PTS))
  local i
  case "$1" in
    score) echo "$SCORE" ;;
    verify)
      echo "Olgunluk: $SCORE/100 | başarılı $PASS, eksik $FAIL"
      for i in "${RESULT[@]}"; do echo "  [$i]"; done
      if [[ "$FAIL" -gt 0 ]]; then
        local min="${MIN_VERIFY_SCORE:-40}"
        if [[ "$SCORE" -lt "$min" ]]; then
          echo "DOĞRULAMA BAŞARISIZ: skor $SCORE < asgari $min" >&2
          exit 1
        else
          echo "UYARI: $FAIL kontrol eksik (skor $min+ olduğu için kabul edildi)"
        fi
      else
        echo "DOĞRULAMA GEÇTİ."
      fi
      ;;
    *)
      echo "── mehmet olgunluk raporu ───────────────────────────"
      for i in "${RESULT[@]}"; do echo "  [$i]"; done
      echo ""
      echo "SKOR: $SCORE/100 | başarılı $PASS, eksik $FAIL"
      echo "KAÇIŞ EŞİĞİ: $ESCAPE_SCORE/100, $ESCAPE_STREAK ardışık iterasyon"
      ;;
  esac
}

record() {
  run_checks
  SCORE=$((PASS * PTS))
  local version prev_streak prev_version streak
  version="$(changelog_version)"
  prev_streak="$(json_field docs/measures.json escape.streak)"
  prev_streak="${prev_streak//[^0-9]/}"
  [[ -z "$prev_streak" ]] && prev_streak=0
  prev_version="$(json_field docs/measures.json version)"
  streak=0
  if [[ "$SCORE" -ge "$ESCAPE_SCORE" ]]; then
    if [[ "$version" == "$prev_version" ]]; then
      streak="$prev_streak"
    else
      streak=$((prev_streak + 1))
    fi
  fi
  node -e '
    const fs=require("fs");
    const v={
      version:process.argv[1]||"0.0.0",
      score:Number(process.argv[2]),
      pass:Number(process.argv[3]),
      fail:Number(process.argv[4]),
      total:Number(process.argv[5]),
      escape:{score:Number(process.argv[6]),streak:Number(process.argv[7]),needed:Number(process.argv[8])},
      updated_at:new Date().toISOString()
    };
    fs.writeFileSync("docs/measures.json",JSON.stringify(v,null,2)+"\n");
    console.log("docs/measures.json güncellendi -> skor "+v.score+"/100, kaçış sayacı "+v.escape.streak);
  ' "$version" "$SCORE" "$PASS" "$FAIL" "$TOTAL_CHECKS" "$ESCAPE_SCORE" "$streak" "$ESCAPE_STREAK"
}

self_test() {
  local before_pass=$PASS before_fail=$FAIL
  PASS=0; FAIL=0; RESULT=()
  run_checks
  if [[ $((PASS + FAIL)) -ne "$TOTAL_CHECKS" ]]; then
    echo "SELF-TEST HATASI: kontrol sayısı $TOTAL_CHECKS olmalı, $((PASS + FAIL)) bulundu" >&2
    exit 1
  fi
  SCORE=$((PASS * PTS))
  echo "SELF-TEST GEÇTİ: $TOTAL_CHECKS kontrol, hesaplanan skor $SCORE/100"
  PASS=$before_pass; FAIL=$before_fail
}

mode="${1:---report}"
case "$mode" in
  --score)  run_checks; render score ;;
  --verify) run_checks; render verify ;;
  --record) record ;;
  --test)   self_test ;;
  *)        run_checks; render report ;;
esac