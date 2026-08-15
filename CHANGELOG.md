# Changelog

## [0.3.0] - 2026-08-15

### Added
- Test altyapısı: `tests/test_project.py` (stdlib unittest, 21 test) proje bütünlüğünü doğrular
- Kaçış/olgunluk metriği: `scripts/maturity.py` 0-100 skor üretir, kaçış eşiğini hesaplar
- CI validation workflow: `.github/workflows/validate.yml` push/PR'da test ve maturity çalıştırır
- `Makefile`: `test`, `maturity`, `check` hedefleri

### Changed
- `.github/workflows/opencode.yml`: action `@latest`'ten `@v1.18.18`'e pinlendi, job'lara 30 dk timeout eklendi

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
