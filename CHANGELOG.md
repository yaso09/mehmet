# Changelog

## [0.3.0] - 2026-08-15

### Added
- `scripts/health-check.sh`: repo sağlık kontrolü + olgunluk (escape) skoru — kaçış mekanizması uygulandı
- `Makefile`: otomasyon hedefleri (`check`, `score`, `json`, `help`)
- GitHub Actions workflow'una `validate` job'ı eklendi (autonomous job öncesi sağlık kontrolü)

### Changed
- README.md'ye olgunluk mekanizması ve geliştirme bölümleri eklendi
- AGENTS.md'ye olgunluk mekanizması bölümü eklendi

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
