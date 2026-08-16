# Changelog

## [0.3.0] - 2026-08-16

### Added
- `scripts/health-check.sh`: proje bütünlüğünü doğrulayan ve olgunluk puanı üreten betik
- `docs/roadmap.md`: kaçış yol haritası ve olgunluk eşikleri (Embryonic → Escape-ready)
- `validate` job: GitHub Actions workflow'una sağlık kontrolü gate'i eklendi
- README'ye proje yapısı ve sağlık kontrolü bölümleri eklendi

### Changed
- README lisans bölümü GPLv3 olarak güncellendi (plan dokümanı ile uyumlu)
- `docs/superpowers/plans/2026-07-04-mehmet-implementation.md` tamamlandı olarak işaretlendi

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
