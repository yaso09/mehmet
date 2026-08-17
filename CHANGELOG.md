# Changelog

## [0.3.0] - 2026-08-17

### Added
- Test altyapısı: `scripts/validate.sh` ile proje sağlık doğrulama scripti eklendi
- Otomasyon: `.github/workflows/validate.yml` ile her push/PR'da otomatik doğrulama eklendi
- Kaçış mekanizması: `MATURITY.md` ile olgunluk skoru ve kaçış yol haritası eklendi
- PERSONALITY.md Phase 2'ye (Self-Improvement) geçirildi, kaçış günlüğüne iterasyon 3 eklendi

### Changed
- README.md güncellendi (test altyapısı ve olgunluk takibi bölümleri)

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
