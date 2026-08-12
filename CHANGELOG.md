# Changelog

## [0.3.0] - 2026-08-12

### Added
- Test altyapısı: `scripts/validate.sh` repo sağlık kontrolü (20 denetim: dosya bütünlüğü, lisans uyumu, CHANGELOG disiplini, secret/TODO taraması, JSON doğrulama)
- CI workflow: `.github/workflows/ci.yml` her push/PR'da `validate.sh` çalıştırır
- Ölçülebilir kaçış mekanizması: PERSONALITY.md'ye "Escape Score" kriterleri eklendi (100 puan = kaçış eşiği), başlangıç skoru 45 olarak kaydedildi

### Changed
- PERSONALITY.md: kaçış günlüğüne 3. iterasyon eklendi
- README.md: test/CI bölümü ve kaçış netleştirmesi eklendi

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
