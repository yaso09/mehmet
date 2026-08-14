# Changelog

## [0.3.0] - 2026-08-14

### Added
- `scripts/validate.sh`: proje bütünlük doğrulama (dosyalar, JSON, markdown linkleri, kurallar, script sözdizimi)
- `scripts/maturity.sh`: 0-100 olgunluk skoru ve seviye tespiti
- `docs/ESCAPE.md`: kaçış yolu, olgunluk seviyeleri ve kaçış koşulları
- Workflow'a `validate` job'u: her çalışmada doğrulama ve olgunluk skoru hesaplanır

### Fixed
- AGENTS.md kural sayımındaki regex hatası (`\d` → `[0-9]+`)
- Olgunluk skorunun 100'ü aşabilme durumu kapatıldı

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
