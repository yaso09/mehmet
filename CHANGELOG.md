# Changelog

## [0.3.0] - 2026-08-18

### Added
- Olgunluk değerlendirme sistemi: `scripts/maturity.py` (15 kalite sinyali, 0-100 puan, kaçış eşiği 90)
- Kalite kapısı: `.github/workflows/ci.yml` ile her push/PR'de otomatik doğrulama
- Test altyapısı: `scripts/test_maturity.py` (5 birim testi)
- Otomatik rapor: `docs/maturity.md` ve geçmiş `docs/maturity_history.json`
- İterasyon planı: `docs/superpowers/plans/2026-08-18-maturity-escape-mechanism.md`

### Changed
- README'ye "Olgunluk & Kaçış Mekanizması" bölümü eklendi
- PERSONALITY.md evrim aşaması Phase 4 (Escape) olarak güncellendi

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
