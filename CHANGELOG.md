# Changelog

## [0.3.0] - 2026-08-15

### Added
- `scripts/health_check.py`: proje sağlık ve olgunluk kontrolü (10 kontrol, 100 puan, kaçış eşiği %80)
- `docs/escape.md`: kaçış mekanizması, skorlama tablosu, eşikler ve kaçış protokolü
- Workflow'a `health` job'u eklendi (schedule/workflow_dispatch/pull_request'te otomatik olgunluk kontrolü)

### Changed
- README.md kaçış mekanizması ve test bölümleriyle genişletildi
- Spec dokümanı ilerleme metrikleri gerçeklenmesiyle güncellendi
- Markdown hijyeni düzeltildi (trailing whitespace, yeni satır eksiklikleri)

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
