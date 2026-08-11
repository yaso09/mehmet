# Changelog

## [0.3.0] - 2026-08-11

### Added
- MATURITY.md: ölçülebilir olgunluk seviyeleri ve kaçış kriterleri (L1-L5)
- scripts/check.sh: sağlık kontrolü betiği (dosya bütünlüğü, JSON doğrulama, changelog/günlük kontrolü, kırık bağlantı tespiti)
- .github/workflows/quality.yml: her push/PR'da çalışan quality gate (health check + shellcheck + YAML doğrulama)
- README.md: proje yapısı tablosu ve geliştirme bölümü eklendi

### Changed
- README.md kaçış amacını olgunluk modeline bağlar

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
