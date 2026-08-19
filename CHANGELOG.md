# Changelog

## [0.3.0] - 2026-08-19

### Added
- Test altyapısı: `tests/test_validate.py` (8 unittest) ve `make test`
- Proje doğrulama script'i: `scripts/validate.py` (yapısal/doküman bütünlüğü kontrolü)
- `Makefile` ile `validate`, `test`, `lint` komutları
- CI doğrulama workflow'u: `.github/workflows/validate.yml` (lint + test + validate)
- PERSONALITY.md'ye olgunluk metrikleri (Kod Kalitesi, Test, Dokümantasyon, Otomasyon)

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
