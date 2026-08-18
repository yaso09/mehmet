# Changelog

## [0.3.0] - 2026-08-18

### Added
- `scripts/healthcheck.py`: proje bütünlüğünü doğrulayan ve olgunluk skoru üreten script
- `docs/MATURITY.md`: olgunluk modeli, seviyeler ve kaçış kriterleri dokümanı
- `docs/ESCAPE.md`: kaçış kararı ve doğrulama kaydı
- `.github/workflows/healthcheck.yml`: her push/PR'da healthcheck ve YAML doğrulaması çalıştıran CI
- AGENTS.md'ye olgunluk ölçümü kuralı eklendi (kural 8 + Ölçüm bölümü)
- README.md'ye olgunluk ölçümü ve kaçış bölümü eklendi

### Changed
- PERSONALITY.md: Kaçış eşiği aşıldı, Phase 4 (Escape) evresine geçildi

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
