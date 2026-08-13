# Changelog

## [0.3.0] - 2026-08-13

### Added
- Test altyapısı: `tests/test_project_health.py` proje yapısını ve dosya tutarlılığını doğrular
- Olgunluk takibi: `scripts/maturity.py` ile 0-100 arası ölçülebilir olgunluk puanı ve METRICS.md geçmişi
- CI workflow'u: `.github/workflows/ci.yml` her push/PR'da test ve olgunluk kontrolü çalıştırır
- Makefile: `make test/validate/maturity/all` hedefleri
- README.md'ye Geliştirme bölümü eklendi

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
