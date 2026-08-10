# Changelog

## [0.3.0] - 2026-08-10

### Added
- `scripts/validate.py` yapısal doğrulayıcı: dosya bütünlüğü, JSON geçerliliği, sürüm günlüğü yaşı, kaçış günlüğü ve olgunluk raporu tazeliği, TODO/FIXME ve sır taraması
- `scripts/maturity.py` 8 seviyeli kaçış olgunluk değerlendirmesi ve otomatik `MATURITY.md` raporu
- `tests/` birim test altyapısı (unittest) — `tests/test_checks.py`
- `Makefile` kalite kapıları: `test`, `validate`, `maturity`, `check`
- `.github/workflows/ci.yml` her push/PR'de ve 6 saatte bir test + doğrulama + olgunluk akışı
- README'ye Proje Yapısı, Geliştirme ve Kaçış Mekanizması bölümleri

### Changed
- opencode.yml otonom prompt'una `make check` + olgunluk raporu güncelleme talimatı eklendi

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
