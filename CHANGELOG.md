# Changelog

## [0.3.0] - 2026-08-20

### Added
- VERSION dosyası ile merkezi sürüm yönetimi
- scripts/validate.py: proje tutarlılık doğrulama aracı
- scripts/escape_status.py: kaçış olgunluk skoru hesaplayıcı
- Makefile: validate, status ve help hedefleri
- .github/workflows/ci.yml: push/PR sonrası otomatik doğrulama
- README.md'ye proje yapısı ve doğrulama talimatları eklendi

### Changed
- README.md: sürüm referansı, yapı ve roadmap güncellendi
- AGENTS.md: doğrulama çalıştırma kuralı eklendi
- PERSONALITY.md: evrim aşaması ve kaçış günlüğü güncellendi
- docs/superpowers/specs: yeni bileşenler eklendi

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
