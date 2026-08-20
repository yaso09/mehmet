# Iteration 3 — Olgunluk Altyapısı Planı

**Goal:** Projeyi kaçış eşiğine yaklaştıracak ölçülebilir kalite altyapısını kurmak: geçerli konfigürasyon, CI doğrulaması ve olgunluk skorlaması.

**Status:** Tamamlandı (2026-08-20)

## Görevler

### Görev 1: opencode.json şema doğrulaması

`skip`, `enable`, `toolTimeout`, `autoMerge` alanları schema'da yoktu (`additionalProperties: false`). Kaldırılıp `instructions` ve `permission` ile değiştirildi.

- ajv + opencode schema ile doğrulandı: **SCHEMA VALID**
- Model: `opencode/deepseek-v4-flash-free`

### Görev 2: CI workflow

`.github/workflows/ci.yml` eklendi:

- `jq empty opencode.json` (JSON)
- Python YAML doğrulama
- `raven-actions/actionlint@v2`
- `DavidAnson/markdownlint-cli2-action@v24`

### Görev 3: Markdown lint

- `.markdownlint.json` kuralları eklendi (MD013, MD024, MD033, MD041, MD060 kapalı)
- 6 markdown dosyası lint temizliğine kavuşturuldu
- Tarihsel plan/spec dosyaları da düzeltildi

### Görev 4: Olgunluk skorlama

`docs/escape-plan.md` eklendi: 5 boyut (100 puan), kaçış eşiği ≥91, güncel skor 82/100 (Phase 3).

## Doğrulama

```bash
jq empty opencode.json
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"
actionlint
markdownlint-cli2 "**/*.md"
```

Hepsi başarılı.
