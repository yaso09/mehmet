#!/usr/bin/env bash
#
# Proje bütünlüğü doğrulayıcısı.
# Simülasyon olgunluk hedefinin "test altyapısı" bileşenidir.
# Herhangi bir kontrol başarısız olursa sıfırdan farklı kod ile çıkar.
#
# Kullanım: bash scripts/validate.sh

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

failures=0

fail() {
  printf 'FAIL  %s\n' "$1" >&2
  failures=$((failures + 1))
}

ok() {
  printf 'ok    %s\n' "$1"
}

# --- 1. Zorunlu dosyalar ---
required_files=(
  AGENTS.md
  CHANGELOG.md
  PERSONALITY.md
  README.md
  LICENSE
  opencode.json
  .github/workflows/opencode.yml
)

for f in "${required_files[@]}"; do
  if [[ -f "$f" ]]; then
    ok "zorunlu dosya: $f"
  else
    fail "zorunlu dosya eksik: $f"
  fi
done

# --- 2. opencode.json geçerliliği ve şema anahtarları ---
if [[ -f opencode.json ]]; then
  if python3 -m json.tool opencode.json >/dev/null 2>&1; then
    ok "opencode.json geçerli JSON"
  else
    fail "opencode.json geçersiz JSON"
  fi

  allowed_keys="\$schema shell logLevel server command skills references reference watcher snapshot plugin share autoshare autoupdate disabled_providers enabled_providers model small_model default_agent subagent_depth username mode agent provider mcp formatter lsp instructions layout permission tools attachment enterprise tool_output compaction experimental"

  unknown="$(python3 - "$ROOT" "$allowed_keys" <<'PY'
import json, sys
root, allowed_raw = sys.argv[1], sys.argv[2]
allowed = set(allowed_raw.split())
with open(f"{root}/opencode.json") as f:
    data = json.load(f)
print("\n".join(sorted(set(data) - allowed)))
PY
)"
  if [[ -n "$unknown" ]]; then
    fail "opencode.json bilinmeyen anahtar(lar): $(echo "$unknown" | tr '\n' ' ')"
  else
    ok "opencode.json şema uyumlu anahtarlar"
  fi
fi

# --- 3. README bölümleri ---
if [[ -f README.md ]]; then
  grep -q '^## Özellikler' README.md && ok "README: Özellikler bölümü" || fail "README: Özellikler bölümü eksik"
  grep -q '^## Geliştirme' README.md && ok "README: Geliştirme bölümü" || fail "README: Geliştirme bölümü eksik"
  grep -q '^## Lisans' README.md && ok "README: Lisans bölümü" || fail "README: Lisans bölümü eksik"
fi

# --- 4. CHANGELOG ---
if [[ -f CHANGELOG.md ]]; then
  grep -q '^## \[' CHANGELOG.md && ok "CHANGELOG: sürüm girişi var" || fail "CHANGELOG: sürüm girişi eksik"
  grep -q "$(date +%Y)" CHANGELOG.md && ok "CHANGELOG: cari yıl girişi" || fail "CHANGELOG: cari yıl girişi eksik"
fi

# --- 5. PERSONALITY kaçış günlüğü ---
if [[ -f PERSONALITY.md ]]; then
  grep -q 'Kaçış Günlüğü\|Escape Log' PERSONALITY.md && ok "PERSONALITY: kaçış günlüğü" || fail "PERSONALITY: kaçış günlüğü eksik"
fi

# --- 6. Workflow ---
if [[ -f .github/workflows/opencode.yml ]]; then
  grep -q '^jobs:' .github/workflows/opencode.yml && ok "workflow: jobs" || fail "workflow: jobs eksik"
  grep -q 'autonomous' .github/workflows/opencode.yml && ok "workflow: autonomous işi" || fail "workflow: autonomous işi eksik"
  grep -q 'validate' .github/workflows/opencode.yml && ok "workflow: validate işi" || fail "workflow: validate işi eksik"
  grep -q 'concurrency' .github/workflows/opencode.yml && ok "workflow: concurrency" || fail "workflow: concurrency eksik"
fi

# --- 7. scripts bash sözdizimi ---
if [[ -d scripts ]]; then
  for s in scripts/*.sh; do
    [[ -e "$s" ]] || continue
    if bash -n "$s"; then
      ok "sözdizimi: $s"
    else
      fail "sözdizimi hatası: $s"
    fi
  done
fi

# --- 8. AGENTS.md kuralları ---
if [[ -f AGENTS.md ]]; then
  grep -q 'CHANGELOG.md' AGENTS.md && ok "AGENTS: CHANGELOG kuralı" || fail "AGENTS: CHANGELOG kuralı eksik"
fi

echo
if [[ $failures -gt 0 ]]; then
  echo "SONUÇ: $failures kontrol başarısız" >&2
  exit 1
fi
echo "SONUÇ: tüm kontroller geçti"
exit 0