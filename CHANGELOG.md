# Changelog

## [0.3.0] - 2026-08-13

### Added
- `scripts/maturity.py`: Proje olgunluğunu 0-100 arası ölçen doğrulama aracı eklendi
- `tests/test_maturity.py`: Maturity checker için 8 birim testi ekledi
- `.github/workflows/validate.yml`: Her push/PR'da olgunluk kontrolü ve testleri çalıştıran CI workflow'u eklendi
- README.md'ye olgunluk sistemi ve test komutları bölümü eklendi
- opencode.json'a `instructions` alanı eklendi (AGENTS.md ve PERSONALITY.md otomatik yüklenir)

### Changed
- Kaçış mekanizması ölçülebilir hale getirildi: olgunluk skoru eşik değerine (70/100) ulaşan proje olgun kabul ediliyor

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
