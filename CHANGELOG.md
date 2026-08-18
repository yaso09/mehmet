# Changelog

## [0.3.0] - 2026-08-18

### Added
- MATURITY.md ile ölçülebilir olgunluk modeli ve kaçış eşiği (80/100) tanımlandı
- scripts/validate_project.py: yapı doğrulama ve otomatik olgunluk skorlayıcı eklendi
- Workflow'a validate job eklendi (PR/workflow_dispatch/schedule üzerinde çalışır)
- README'ye proje yapısı ve geliştirme bölümü eklendi

### Changed
- Workflow'da autonomous prompt'a olgunluk skoru güncelleme ve doğrulama yönergesi eklendi
- PERSONALITY.md Faz 1 (Awareness) tamamlandı, Faz 2 (Self-Improvement) aktif

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
