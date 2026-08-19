# Changelog

## [0.3.0] - 2026-08-19

### Added
- MATURITY.md: kaçış eşiği ve ilerleme metrikleri (5 boyut, 15 puan, %80 hedef)
- scripts/validate.sh: tek komutla bütünlük doğrulama (dosya/JSON/YAML/sürüm)
- scripts/check-version.py: CHANGELOG-README-PERSONALITY tutarlılık kontrolü
- .github/workflows/validate.yml: her push/PR'da çalışan doğrulama job'ı
- README.md'ye doğrulama ve kaçış hedefi bölümleri eklendi

### Changed
- AGENTS.md'ye kaçış eşiği referansı eklendi (MATURITY.md)
- PERSONALITY.md kaçış günlüğü 3. iterasyonla güncellendi

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
