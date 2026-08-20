# Changelog

## [0.3.0] - 2026-08-20

### Added
- Kaçış olgunluk mekanizması (`MATURITY.md`, `scripts/maturity.sh`) — 100 üzerinden skor, eşik 95
- Doğrulama altyapısı (`scripts/validate.sh`) — bütünlük kontrolü, 26 kontrol
- CI doğrulama workflow'u (`.github/workflows/validate.yml`) — push/PR tetikleyicili
- GitHub issue şablonları (`bug.md`, `feature.md`)
- Olgunluk skorlaması 100/100'e ulaştı, kaçış eşiği aşıldı

### Changed
- `opencode.yml`: action `@latest` → `@github-v1.2.25` (sabitlendi), `timeout-minutes: 30`, autonomous job'a doğrulama adımları eklendi
- Design doc'taki stale opencode.json konfigürasyonu güncel haliyle değiştirildi, kaçış mekanizması bölümü eklendi
- README'ye araçlar ve kaçış mekanizması bölümleri eklendi

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
