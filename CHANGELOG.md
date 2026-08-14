# Changelog

## [0.3.0] - 2026-08-14

### Added
- `scripts/maturity.mjs` — kaçış eşiği (75/100) bazlı olgunluk değerlendirme script'i
- Test altyapısı: `tests/maturity.test.mjs` (node:test, 7 test) ve `package.json`
- `npm test` / `npm run verify` script'leri
- GitHub Actions workflow'una `verify` job'u (test + olgunluk raporu)
- README'ye Olgunluk ve Geliştirme bölümleri

### Fixed
- `maturity.mjs` CHANGELOG sürüm kontrolü çok satırlı moda geçirildi

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
