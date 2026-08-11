# Changelog

## [0.3.0] - 2026-08-11

### Added
- `scripts/validate.sh`: proje sağlığı için otomatik doğrulama (JSON/YAML/artifact formatı) — ilk test altyapısı
- `.github/workflows/ci.yml`: push/PR'lerde `validate.sh`'i çalıştıran CI workflow'u
- `docs/maturity.md`: kaçış eşiğini tanımlayan olgunluk modeli (23 makineyle kontrol edilebilir kriter, 4 kategori)
- `scripts/maturity.sh`: olgunluk skoru hesaplayan script (100 üzerinden puan + seviye)
- `docs/superpowers/plans/2026-08-11-mehmet-maturity-validation.md`: bu iterasyonun uygulama planı

### Changed
- `.github/workflows/opencode.yml`'deki `autonomous` ve `comment` job'larına `timeout-minutes: 30` eklendi

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
