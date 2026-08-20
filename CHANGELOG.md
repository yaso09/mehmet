# Changelog

## [0.3.0] - 2026-08-20

### Added
- `scripts/maturity.sh`: 100 puan üzerinden kaçış/olgunluk ölçer (eşik: 80)
- `scripts/check.sh`: Yapısal doğrulama ve test altyapısı (17 kontrol)
- `.github/workflows/ci.yml`: Push/PR üzerinde kontrolleri çalıştıran CI workflow'u
- `Makefile`: `make check`, `make maturity`, `make escape` otomasyon komutları
- README.md'ye proje yapısı ve kaçış mekanizması dokümantasyonu eklendi

### Changed
- Evrim aşaması "Awareness"tan "Self-Improvement"a geçti (PERSONALITY.md)

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
