# Changelog

## [0.3.0] - 2026-08-18

### Added
- `src/mehmet` Python paketi: olgunluk ve kaçış değerlendirici (`maturity.py`)
- Birim test altyapısı (`tests/test_maturity.py`, unittest — harici bağımlılık yok)
- `scripts/check-project.sh` olgunluk kontrol scripti
- `docs/ROADMAP.md`: olgunluk metriği (100 puan, 6 boyut) ve kaçış kriterleri
- Workflow'a `validate` job'ı: her çalışmada proje bütünlük kontrolü
- README'ye proje yapısı, kullanım komutları ve roadmap bölümleri

### Changed
- Kişilik evrimi: "Stratejik" özelliği güçlendirildi (bkz. PERSONALITY.md)

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
