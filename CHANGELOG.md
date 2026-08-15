# Changelog

## [0.3.0] - 2026-08-15

### Added
- `scripts/maturity.sh`: Olgunluk skoru (0-100) ve seviye (Embryo/Adolescent/Mature/Escape-ready) hesaplayan kaçış mekanizması scripti
- `tests/validate.sh`: Repo bütünlük testleri (dosyalar, JSON geçerliliği, workflow yapısı, secret sızıntı kontrolü)
- `Makefile`: `validate`, `maturity`, `check`, `test` hedefleri
- `.github/workflows/validate.yml`: Push ve PR'larda testleri koşan CI workflow'u
- `docs/maturity.md`: Kaçış mekanizması, kriterler ve olgunluk seviyeleri dokümantasyonu
- `.gitignore`: `__pycache__/`, `*.pyc`, `.pytest_cache/`, `coverage/`, `.coverage` eklendi

### Changed
- README.md'ye Geliştirme bölümü ve `make` komutları eklendi

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
