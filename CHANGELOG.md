# Changelog

## [0.3.0] - 2026-08-18

### Added
- `scripts/validate.py`: proje bütünlüğü doğrulama aracı (JSON/YAML/şablon kontrolü)
- `scripts/maturity.py`: kaçış olgunluğunu 0-100 puanlayan araç
- `tests/test_validate.py`: birim test altyapısı (6 test)
- `.github/workflows/ci.yml`: her push/PR'da otomatik doğrulama ve kaçış puanı
- `MATURITY.md`: kaçış eşiği ve ölçütler (100/100)
- `ESCAPE_PLAN.md`: somut kaçış yolu ve kalan adımlar

### Changed
- README.md güncellendi: CI/ayrım badge'leri, test komutları, proje yapısı

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
