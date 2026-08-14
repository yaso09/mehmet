#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAILED=0

log_ok()  { printf '  \033[32m✔\033[0m %s\n' "$1"; }
log_fail(){ printf '  \033[31m✘\033[0m %s\n' "$1"; FAILED=1; }
section(){ printf '\n\033[1m%s\033[0m\n' "$1"; }

section "Zorunlu dosyalar"
for f in AGENTS.md README.md CHANGELOG.md PERSONALITY.md opencode.json .github/workflows/opencode.yml LICENSE; do
  if [[ -f "$ROOT/$f" ]]; then
    log_ok "$f"
  else
    log_fail "eksik: $f"
  fi
done

section "JSON geçerliliği"
if command -v python3 >/dev/null 2>&1; then
  for f in opencode.json; do
    if python3 -c "import json,sys; json.load(open('$ROOT/$f'))" 2>/dev/null; then
      log_ok "$f geçerli JSON"
    else
      log_fail "$f geçersiz JSON"
    fi
  done
else
  log_fail "python3 bulunamadı, JSON doğrulaması atlandı"
fi

section "Markdown referansları"
if command -v python3 >/dev/null 2>&1; then
  MISSING=$(python3 - "$ROOT" <<'EOF'
import os, re, sys
root = sys.argv[1]
missing = []
for f in ("README.md", "CHANGELOG.md"):
    path = os.path.join(root, f)
    if not os.path.exists(path):
        continue
    text = open(path, encoding="utf-8").read()
    for m in re.findall(r'\]\(([^)]+\.md)\)', text):
        ref = m.split("#")[0]
        if ref and not os.path.exists(os.path.join(root, ref)):
            missing.append(f"{f} -> {m}")
print("\n".join(missing))
EOF
)
  if [[ -z "$MISSING" ]]; then
    log_ok "tüm markdown bağlantıları geçerli"
  else
    echo "$MISSING" | while IFS= read -r line; do log_fail "kırık bağlantı: $line"; done
  fi
fi

section "CHANGELOG kontrolü"
if grep -q "^## \[" "$ROOT/CHANGELOG.md" 2>/dev/null; then
  log_ok "CHANGELOG sürüm girişleri mevcut"
else
  log_fail "CHANGELOG'da sürüm girişi yok"
fi

section "AGENTS.md kuralları"
RULES=$(grep -cE "^[0-9]+\." "$ROOT/AGENTS.md" 2>/dev/null || true)
if [[ "$RULES" -ge 7 ]]; then
  log_ok "7 simülasyon kuralı mevcut"
else
  log_fail "AGENTS.md kuralları eksik (bulunan: $RULES)"
fi

section "Script sözdizimi"
for s in "$ROOT"/scripts/*.sh; do
  [[ -e "$s" ]] || continue
  if bash -n "$s" 2>/dev/null; then
    log_ok "$(basename "$s") sözdizimi geçerli"
  else
    log_fail "$(basename "$s") sözdizimi hatası"
  fi
done

printf '\n'
if [[ "$FAILED" -eq 0 ]]; then
  printf '\033[32mDoğrulama başarılı.\033[0m\n'
  exit 0
else
  printf '\033[31mDoğrulama başarısız.\033[0m\n'
  exit 1
fi