# Changelog

## [0.3.0] - 2026-08-12

### Added
- `scripts/healthcheck.py`: proje sağlık kontrolü ve olgunluk (maturity 0-10) skorlayıcısı
- `.github/workflows/ci.yml`: her push/PR'da healthcheck'i çalıştıran CI test altyapısı
- `docs/escape-plan.md`: olgunluk modeli ve ölçülebilir kaçış kriterleri (escape thresholds)
- README.md'ye Proje Yapısı, Sağlık & Olgunluk, Etkileşim ve Yönetim bölümleri
- AGENTS.md'ye healthcheck çalıştırma ve kaçış planı takibi kuralları (8, 9)

### Changed
- CHANGELOG.md, README.md, PERSONALITY.md, AGENTS.md consistency düzenlendi
- PERSONALITY.md: evrim aşaması Faz 2 (Self-Improvement) olarak güncellendi

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
