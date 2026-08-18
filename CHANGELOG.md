# Changelog

## [0.3.0] - 2026-08-18

### Added
- Test altyapısı eklendi (unittest, 17 test): `tests/test_validate.py` ve `tests/test_maturity.py`
- `scripts/validate.py` — proje yapısını doğrulayan 12 kontrol (JSON/CHANGELOG/README/workflow vb.)
- `scripts/maturity.py` — kaçış/olgunluk skoru hesaplayan araç (0-100, eşik: 80)
- `.github/workflows/ci.yml` — her push/PR'da validate + test + maturity çalıştıran CI
- `Makefile` — `make validate`, `make test`, `make maturity` hedefleri

### Fixed
- `scripts/maturity.py` sayesinde kaçış skoru artık ölçülebilir (şu an 100/100)

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
