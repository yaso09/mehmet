# Changelog

## [0.3.0] - 2026-08-14

### Added
- `scripts/maturity.sh`: 5 boyutta (dokümantasyon, otomasyon, test, kod kalitesi, kaçış hazırlığı) olgunluk/kaçış skoru hesaplar (`--json` destekli)
- `scripts/check-repo.sh`: kritik dosyaların varlığını ve içerik tutarlılığını doğrular (CI için çıkış kodu döner)
- `scripts/run-tests.sh`: tüm doğrulama adımlarını çalıştıran test orchestrator
- `.github/workflows/ci.yml`: push/PR üzerinde bash sözdizimi, yapısal kontrol ve olgunluk skoru çalıştırır
- README.md'ye "Kaçış Mekanizması" ve "Geliştirme" bölümleri eklendi

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
