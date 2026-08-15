# Changelog

## [0.3.0] - 2026-08-15

### Added
- `scripts/maturity.py`: Kaçış hedefi için olgunluk (maturity) puanlama mekanizması
- `tests/test_maturity.py`: 12 ünite testi (stdlib unittest tabanlı)
- `Makefile`: test, maturity, report, check, clean görevleri
- `.github/workflows/ci.yml`: Push/PR'da test + maturity raporu çalıştıran CI job'u
- `docs/maturity-report.md`: Otomatik üretilen olgunluk raporu

### Changed
- `opencode.json` config'i maturity skorlamasında daha detaylı puanlanıyor
- Design spec'teki "Gelecek Geliştirmeler" tamamlanan maddeler işaretlendi

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
