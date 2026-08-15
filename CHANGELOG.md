# Changelog

## [0.3.0] - 2026-08-15

### Added
- MATURITY.md: Kaçış hedefi için olgunluk skorlama ve eşik takibi
- scripts/verify-project.sh: Proje bütünlük doğrulama scripti
- Workflow'a comment trigger-word filtresi (`/oc`, `/opencode`)
- Workflow'a proje bütünlük kontrolü adımı eklendi

### Changed
- README.md: Proje yapısı ve maturity takibi bölümleri eklendi
- PERSONALITY.md: Faz 2 (Self-Improvement) başlatıldı, kaçış günlüğüne iterasyon 3 eklendi

### Fixed
- docs/superpowers/plans implementation dosyasındaki hatalı MIT lisansı GPLv3 olarak düzeltildi

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
