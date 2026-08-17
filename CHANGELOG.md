# Changelog

## [0.3.0] - 2026-08-17

### Added
- ESCAPE.md ile ölçülebilir kaçış mekanizması eklendi (olgunluk seviyeleri, skor kartı, kaçış kapıları, kaçış protokolü)
- Test altyapısı eklendi: `scripts/validate.sh` proje doğrulama betiği
- CI otomasyonu eklendi: `.github/workflows/validate.yml` her push'ta doğrulama çalıştırır
- README.md'ye proje yapısı, escape durumu ve workflow badge'leri eklendi

### Changed
- AGENTS.md'ye 8. kural eklendi (ESCAPE.md güncelleme + validate.sh doğrulama)
- README.md escape mekanizması bilgisiyle güncellendi

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
