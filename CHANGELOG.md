# Changelog

## [0.3.0] - 2026-08-18

### Added
- Test altyapısı: `scripts/check_project.py` — bağımlılıksız proje bütünlük denetimi
- Makefile: `make check` / `make test` hedefleri
- CI doğrulama workflow'u: `.github/workflows/validate.yml` (her push/PR'da çalışır)
- Olgunluk modeli: `docs/MATURITY.md` (6 seviyeli kaçış rubriği)

### Changed
- AGENTS.md: `make check` zorunluluğu ve olgunluk takibi kuralları eklendi
- README.md: Kalite Kontrol ve Olgunluk Takibi bölümleri eklendi

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
