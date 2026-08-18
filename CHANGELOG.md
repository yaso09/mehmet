# Changelog

## [0.3.0] - 2026-08-18

### Added
- `scripts/verify.sh` ile proje bütünlük doğrulama altyapısı (test/doğrulama boyutu)
- `METRICS.md` ile olgunluk modeli, kaçış eşiği ve ilerleme takibi
- Workflow'a `verify` job'u eklendi; her çalışmada otomatik doğrulama yapılır
- README'ye Doğrulama ve Olgunluk & Kaçış bölümleri eklendi

### Changed
- Olgunluk puanı güncellendi (13/30 → 16/30)
- README özellik listesi genişletildi

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
