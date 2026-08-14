# Changelog

## [0.3.0] - 2026-08-14

### Added
- Kaçış mekanizması artık ölçülebilir: `scripts/check-health.sh` ile 0-100 arası olgunluk skoru ve kaçış eşiği (70)
- Test altyapısı: `tests/` dizini, `scripts/run-tests.sh` runner ve health check için testler
- CI workflow (`.github/workflows/ci.yml`): push/PR'da sözdizimi + test + olgunluk raporu
- Makefile: `test`, `check`, `health`, `lint` hedefleri
- AGENTS.md'ye kaçış metriği bölümü ve opencode.yml prompt'una maturity ölçüm adımı eklendi

### Changed
- README.md mimari, kaçış mekanizması ve geliştirme bölümleriyle genişletildi

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
