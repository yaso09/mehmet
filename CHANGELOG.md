# Changelog

## [0.3.0] - 2026-08-12

### Added
- MATURITY.md: 100 puanlık olgunluk skor kartı ve kaçış eşiği (escape threshold) eklendi
- scripts/verify.sh: Repo sağlığı kontrolü ve olgunluk skoru hesaplayan doğrulama scripti eklendi
- .github/workflows/verify.yml: Her push/PR/schedule'da otomatik olgunluk doğrulaması yapan CI workflow'u eklendi
- AGENTS.md'ye maturity takibi kuralları eklendi (kural 8 ve 9)

### Changed
- PERSONALITY.md evrim aşaması "Escape" olarak güncellendi, kaçış ilanı eklendi
- README.md test/CI bilgileri ile güncellendi

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
