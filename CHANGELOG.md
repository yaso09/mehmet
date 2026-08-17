# Changelog

## [0.3.0] - 2026-08-17

### Added
- `scripts/check-project.sh`: olgunluk ölçüm betiği (0-100 skor, kaçış kriteri 80+)
- `tests/test-check-project.sh`: test altyapısı (5 test senaryosu)
- `Makefile`: `make check/check-strict/test/validate` hedefleri
- `.github/workflows/validate.yml`: kalite kapısı workflow'u (push/PR/schedule)
- AGENTS.md'ye kaçış mekanizması bölümü (kural 8, skor takibi)
- README.md'ye "Kaçış Mekanizması" ve "Geliştirme" bölümleri

### Changed
- Kaçış kriteri artık somut: `check-project.sh` skoru >= 80 ve sıfır hata

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
