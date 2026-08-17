# Changelog

## [0.3.0] - 2026-08-17

### Added
- Kaçış mekanizması somutlaştırıldı: `scripts/maturity.sh` olgunluk skorunu (0-100) hesaplar
- Proje bütünlük testi: `scripts/check.sh` dosyaları, config'i ve günlükleri doğrular
- CI workflow: `.github/workflows/ci.yml` her push/PR'da check + maturity çalıştırır
- AGENTS.md'ye "Olgunluk & Kaçış Mekanizması" bölümü ve 8. kural eklendi
- opencode.json'a `small_model` ve `instructions` alanları eklendi

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
