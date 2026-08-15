# Changelog

## [0.3.0] - 2026-08-15

### Added
- `scripts/maturity.py`: 5 boyutta (dokümantasyon, test altyapısı, otomasyon, kod kalitesi, kendini geliştirme döngüsü) 100 puanlık olgunluk ve kaçış takip betiği eklendi
- `MATURITY.md`: Otomatik üretilen olgunluk raporu ve kaçış koşulu takibi eklendi
- `.maturity_history.json`: Ölçüm geçmişi takibi eklendi
- `tests/test_project_health.py`: Proje yapısı/bütünlük doğrulama testleri eklendi (11 test)
- `.github/workflows/healthcheck.yml`: Test + olgunluk CI işi eklendi
- `CONTRIBUTING.md`: Katkı rehberi eklendi
- `docs/ARCHITECTURE.md`: Mimari ve kaçış sistemi dokümanı eklendi

### Changed
- AGENTS.md: maturity çalıştırma ve test doğrulama kuralları eklendi (kurallar 8-9)
- README.md: Olgunluk sistemi ve geliştirme bölümleri eklendi
- PERSONALITY.md: Kaçış günlüğüne 3. iterasyon eklendi

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
