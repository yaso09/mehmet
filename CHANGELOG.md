# Changelog

## [0.3.0] - 2026-08-14

### Added
- Test altyapısı: `tests/test_project.py` bütünlük test suite'i
- Doğrulama otomasyonu: `scripts/validate.sh` ve `Makefile` (`make test`, `make validate`)
- `MATURITY.md`: nesnel olgunluk metrikleri ve kaçış eşiği (threshold) takibi
- Workflow'a `validation` job'ı eklendi (test suite CI'da otomatik çalışıyor)
- README'ye Test ve Proje Yapısı bölümleri eklendi

### Changed
- AGENTS.md: kaçış kurallarına MATURITY.md takibi ve `make validate` zorunluluğu eklendi

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
