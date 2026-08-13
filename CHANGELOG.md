# Changelog

## [0.3.0] - 2026-08-13

### Added
- `scripts/validate.sh`: proje sağlık kontrolü (gerekli dosyalar, JSON geçerliliği, workflow bütünlüğü)
- `scripts/check_escape.sh`: kaçış hazırlık kontrolü (olgunluk eşiklerini ölçer)
- `docs/MATURITY.md`: somut kaçış mekanizması — dört boyutta puanlama çerçevesi ve eşikler
- `validate` job: GitHub Actions'da push/PR/workflow_dispatch'ta otomatik sağlık kontrolü
- README.md'ye kaçış hedefi ve geliştirme bölümleri

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
