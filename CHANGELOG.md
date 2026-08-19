# Changelog

## [0.3.0] - 2026-08-19

### Added
- `scripts/validate_project.py`: proje sağlık kontrolü ve olgunluk skorlama
- `METRICS.md`: kaçış olgunluğu skorlama tablosu ve eşik tanımı (80/90)
- `tests/test_validate_project.py`: doğrulama script'i için unittest altyapısı
- Workflow'a `validate` job'ı (doğrulama + test), her job'a `timeout-minutes`

### Changed
- AGENTS.md kaçış mekanizması `METRICS.md` ve `scripts/validate_project.py`'ye bağlandı
- README.md'ye proje sağlığı ve doğrulama komutları bölümü eklendi

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
