# Changelog

## [0.3.0] - 2026-08-20

### Added
- `scripts/mehmet_health.py`: olgunluk/maturity skorlama, AGENTS.md kurallarını doğrulayan sağlık kontrolü ve kaçış eşiği (80/100) CLI aracı
- `scripts/tests/test_health.py`: 17 birim testi
- `Makefile`: `check`, `test`, `health`, `report` hedefleri
- `VERSION`: semantik versiyon takibi
- `docs/health-report.md`: otomatik üretilen sağlık raporu
- Workflow'a `validate` job'u: PR/push'ta test + sağlık kontrolü (API key gerektirmez)

### Changed
- README.md'ye geliştirme/doğrulama bölümü eklendi
- `count_files_matching` ile test/script algılama iyileştirildi

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
