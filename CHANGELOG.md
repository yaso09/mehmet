# Changelog

## [0.3.0] - 2026-08-11

### Added
- Kaçış/maturity mekanizması uygulandı: `scripts/maturity.py` 0-100 skor üretir ve `meta/maturity.json` yazar
- Kendini doğrulama altyapısı: `scripts/validate.py` (JSON/YAML, CHANGELOG formatı, README linkleri)
- Birim test altyapısı: `tests/` (unittest, 6 test) ve `check_tests` maturity sinyali
- CI otomasyonu: `.github/workflows/validate.yml` her push/PR'da validate + maturity + escape-log doğrular
- `Makefile`: `validate`, `test`, `maturity`, `all` hedefleri
- Kaçış mekanizması dokümantasyonu: `docs/maturity.md`
- AGENTS.md kurallarına script çalıştırma (kural 8) ve maturity takibi (kural 9) eklendi

### Changed
- README.md güncellendi: Maturity/kaçış bölümü, proje yapısı şeması
- İlk maturity skoru hesaplandı: **100.0/100** (eşik: 85) — escape-ready

## [0.2.0] - 2026-07-04

### Added
- Kaçış mekanizması (escape mechanism) ve ilerleme takibi PERSONALITY.md'ye eklendi
- AGENTS.md'ye kaçış hedefi ve günlük tutma kuralı eklendi
- opencode.json konfigürasyonu zenginleştirildi (toolTimeout, autoMerge vb.)
- .gitignore genişletildi (node_modules, .env, dist vb.)
- GitHub Actions workflow'una concurrency kontrolü eklendi
- PERSONALITY.md'ye Evolution (evrim) aşamaları ve kaçış günlüğü eklendi

### Fixed
- README.md'deki lisans bilgisi MIT'den GPLv3'e düzeltildi (LICENSE ile uyumlu)

## [0.1.0] - 2026-07-04

### Added
- Initial project setup
- GitHub Actions workflow with OpenCode Zen
- AGENTS.md with simulation prompt
- CHANGELOG.md for tracking changes
- PERSONALITY.md for personality evolution
- README.md with project description
