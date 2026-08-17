#!/usr/bin/env bash
#
# validate.sh — mehmet proje sağlık kontrolü
#
# Projenin bütünlüğünü doğrular. GitHub Actions 'validate' işinde ve
# yerel geliştirmede kullanılır. Her kontrol PASS/FAIL olarak raporlanır;
# herhangi bir FAIL varsa çıkış kodu 1 olur.
#
# Kullanım: ./scripts/validate.sh

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAILURES=0
PASSES=0

report() {
  local status="$1"
  local name="$2"
  if [[ "$status" == "FAIL" ]]; then
    echo "  FAIL  $name"
    FAILURES=$((FAILURES + 1))
  else
    echo "  PASS  $name"
    PASSES=$((PASSES + 1))
  fi
}

check() {
  local name="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    report "PASS" "$name"
  else
    report "FAIL" "$name"
  fi
}

echo "mehmet proje doğrulaması"
echo "------------------------"

# 1. Zorunlu dosyalar mevcut olmalı
REQUIRED_FILES=(
  "AGENTS.md"
  "README.md"
  "CHANGELOG.md"
  "PERSONALITY.md"
  "LICENSE"
  "opencode.json"
  ".github/workflows/opencode.yml"
)
for f in "${REQUIRED_FILES[@]}"; do
  check "zorunlu dosya: $f" test -f "$ROOT/$f"
done

# 2. opencode.json geçerli JSON ve top-level anahtarları schema ile uyumlu
if command -v python3 >/dev/null 2>&1; then
  ALLOWED_KEYS='$schema model small_model shell logLevel server command skills references reference watcher snapshot plugin share autoshare autoupdate disabled_providers enabled_providers default_agent subagent_depth username mode agent provider mcp formatter lsp instructions layout permission tools attachment enterprise tool_output compaction experimental'

  python3 - "$ROOT/opencode.json" "$ALLOWED_KEYS" <<'PY'
import json, sys
path, allowed = sys.argv[1], sys.argv[2].split()
try:
    with open(path) as f:
        cfg = json.load(f)
except Exception as e:
    print(f"geçersiz JSON: {e}")
    sys.exit(1)
unknown = sorted(set(cfg.keys()) - set(allowed))
if unknown:
    print(f"geçersiz anahtarlar: {', '.join(unknown)}")
    sys.exit(1)
if "model" not in cfg or "/" not in cfg["model"]:
    print("model anahtarı eksik veya hatalı")
    sys.exit(1)
sys.exit(0)
PY
  if [[ $? -eq 0 ]]; then
    report "PASS" "opencode.json geçerli JSON + schema uyumlu anahtarlar"
  else
    report "FAIL" "opencode.json geçerli JSON + schema uyumlu anahtarlar"
  fi
else
  report "FAIL" "python3 bulunamadı (opencode.json doğrulanamadı)"
fi

# 3. README lisansı LICENSE dosyasıyla tutarlı olmalı
if grep -q "GNU GENERAL PUBLIC LICENSE" "$ROOT/LICENSE" 2>/dev/null; then
  if grep -qi "GPL" "$ROOT/README.md" 2>/dev/null; then
    report "PASS" "README lisans GPLv3 ile tutarlı"
  else
    report "FAIL" "README lisans GPLv3 ile tutarlı"
  fi
else
  report "FAIL" "LICENSE GPLv3 imzası taşıyor"
fi

# 4. CHANGELOG.md bir sürüm başlığı içermeli
if grep -Eq "^## \[[0-9]+\.[0-9]+\.[0-9]+\]" "$ROOT/CHANGELOG.md" 2>/dev/null; then
  report "PASS" "CHANGELOG.md sürüm başlığı içeriyor"
else
  report "FAIL" "CHANGELOG.md sürüm başlığı içeriyor"
fi

# 5. Workflow YAML'i ayrıştırılabilir olmalı
if command -v ruby >/dev/null 2>&1; then
  if ruby -ryaml -e "YAML.load_file('$ROOT/.github/workflows/opencode.yml'); exit 0" >/dev/null 2>&1; then
    report "PASS" "workflow YAML ayrıştırılabilir"
  else
    report "FAIL" "workflow YAML ayrıştırılabilir"
  fi
else
  report "FAIL" "ruby bulunamadı (YAML doğrulanamadı)"
fi

# 6. opencode.json model ile workflow modeli tutarlı olmalı
CFG_MODEL="$(python3 -c "import json;print(json.load(open('$ROOT/opencode.json')).get('model',''))" 2>/dev/null)"
WF_MODEL="$(grep -Eo 'model: [^ ]+' "$ROOT/.github/workflows/opencode.yml" | head -1 | awk '{print $2}')"
if [[ -n "$CFG_MODEL" && "$CFG_MODEL" == "$WF_MODEL" ]]; then
  report "PASS" "model tutarlılığı ($CFG_MODEL)"
else
  report "FAIL" "model tutarlılığı (config=$CFG_MODEL, workflow=$WF_MODEL)"
fi

# 7. PERSONALITY.md kaçış günlüğü tablosu içermeli
if grep -q "Kaçış Günlüğü / Escape Log" "$ROOT/PERSONALITY.md" 2>/dev/null; then
  report "PASS" "PERSONALITY.md kaçış günlüğü içeriyor"
else
  report "FAIL" "PERSONALITY.md kaçış günlüğü içeriyor"
fi

# 8. Git çalışma ağacı temiz olmalı (değişiklikler kaydedilmeli)
if git -C "$ROOT" diff --quiet 2>/dev/null; then
  report "PASS" "git çalışma ağacı temiz"
else
  report "FAIL" "git çalışma ağacı temiz"
fi

echo "------------------------"
echo "Sonuç: $PASSES PASS, $FAILURES FAIL"

# 9. Olgunluk skoru (escape hedefi için ölçülebilir ilerleme)
maturity_score() {
  local score=0
  # Test/doğrulama altyapısı
  if [[ -f "$ROOT/scripts/validate.sh" ]]; then score=$((score + 2)); fi
  if [[ -f "$ROOT/.github/workflows/validate.yml" ]]; then score=$((score + 2)); fi
  # Otomasyon
  if grep -q "schedule:" "$ROOT/.github/workflows/opencode.yml" 2>/dev/null; then score=$((score + 2)); fi
  if grep -q "concurrency:" "$ROOT/.github/workflows/opencode.yml" 2>/dev/null; then score=$((score + 1)); fi
  # Dokümantasyon ve bakım
  if grep -Eq "^## \[[0-9]+\.[0-9]+\.[0-9]+\]" "$ROOT/CHANGELOG.md" 2>/dev/null; then score=$((score + 1)); fi
  if grep -q "Kaçış Günlüğü / Escape Log" "$ROOT/PERSONALITY.md" 2>/dev/null; then score=$((score + 1)); fi
  if [[ -d "$ROOT/docs" ]]; then score=$((score + 1)); fi
  echo "$score"
}

SCORE="$(maturity_score)"
echo "Olgunluk Skoru: $SCORE/10"
echo "Kaçış hedefi: 10/10'a ulaşmak (Phase 4: Escape)."

if [[ $FAILURES -gt 0 ]]; then
  exit 1
fi
exit 0