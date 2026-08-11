# Changelog

## [0.3.0] - 2026-08-11

### Added
- `scripts/check.sh` repo sağlık kontrolü ve olgunluk puanı (maturity score) ölçümü
- `.github/workflows/check.yml` CI workflow'u (her push/PR'da sağlık kontrolü)
- `docs/escape-plan.md` ölçülebilir kaçış kriterleri (5 seviye)
- README'ye Durum, Yol Haritası ve self-check özelliği eklendi

### Changed
- README.md sürüm 0.3.0 olarak güncellendi
- AGENTS.md kaçış planına referans verecek şekilde güncellendi

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
