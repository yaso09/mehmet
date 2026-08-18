# Changelog

## [0.3.0] - 2026-08-18

### Added
- `scripts/validate.py`: proje tutarlılık doğrulama aracı (dosyalar, opencode.json, workflow, dokümantasyon)
- `scripts/maturity.py`: 0-100 kaçış/olgunluk skoru hesaplama aracı (5 boyut: yapılandırma, workflow, dokümantasyon, test, otomasyon)
- `tests/`: 25 unittest testi (`test_validate.py`, `test_maturity.py`)
- `.github/workflows/ci.yml`: push/PR'da test, doğrulama ve olgunluk kontrolleri
- `Makefile`: `make test`, `make validate`, `make maturity`, `make ci` komutları
- `MATURITY.md`: kaçış/olgunluk raporu (92/100 — kaçış eşiğine ulaşıldı)
- AGENTS.md'ye test/doğrulama ve olgunluk takibi kuralları (8, 9) eklendi

### Changed
- README.md'ye Geliştirme bölümü ve yeni özellikler eklendi
- Design doc'a durum notu eklendi, uygulanan "Gelecek Geliştirmeler" işaretlendi
- Test hataları düzeltildi, tüm testler geçiyor

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
