# Changelog

## [0.3.0] - 2026-08-15

### Added
- `scripts/validate.sh`: Repo sağlık kontrolü (zorunlu dosyalar, CHANGELOG formatı, README bölümleri, sır/anahtar taraması, script izinleri)
- `scripts/maturity.sh`: Kaçış mekanizması — olgunluk skoru ve seviye hesaplama (Embryo → Escaped); `--write` ile MATURITY.md'yi günceller
- `scripts/test.sh`: Test suite — validate ve maturity scriptlerinin davranışını test eder (7 test)
- `MATURITY.md`: Olgunluk ve kaçış takip dosyası
- `CONTRIBUTING.md`: Katkı rehberi ve geliştirme döngüsü dokümantasyonu
- Workflow'a doğrulama ve test adımı eklendi (her çalışmadan önce validate.sh + test.sh + maturity.sh --write)

### Changed
- README.md: Doğrulama/olgunluk bölümü ve katkı linki eklendi

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
