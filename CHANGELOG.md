# Changelog

## [0.3.0] - 2026-08-17

### Added
- `scripts/self_assess.sh`: 100 üzerinden olgunluk skoru üreten kaçış mekanizması ölçüm aracı
- `scripts/run_tests.sh`: kabuk tabanlı test çalıştırıcı
- `tests/`: 5 test (dokümantasyon, konfigürasyon, güvenlik, workflow, olgunluk)
- `.github/workflows/checks.yml`: CI — testler, shellcheck, YAML/JSON doğrulama, olgunluk eşiği
- `docs/maturity.md` ve `docs/maturity.json`: olgunluk raporu (100/100)
- `docs/ARCHITECTURE.md`: mimari dokümantasyonu
- `CONTRIBUTING.md`: katkı rehberi

### Changed
- `AGENTS.md`: olgunluk ölçümü ve doğrulama adımları eklendi
- `.github/workflows/opencode.yml`: `timeout-minutes: 15` eklendi (sonsuz döngü koruması)
- `README.md`: test ve olgunluk takibi bilgileri eklendi

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
