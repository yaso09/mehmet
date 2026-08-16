# Changelog

## [0.3.0] - 2026-08-16

### Added
- Kaçış olgunluk motoru `scripts/maturity.py` eklendi (0-100 skor, 4 boyut, kaçış eşiği 80/100)
- `tests/test_maturity.py` ile motor için 7 birim testi eklendi
- GitHub Actions CI workflow'u (`.github/workflows/ci.yml`) eklendi: test + olgunluk değerlendirmesi + gate
- Makefile eklendi (`make test`, `make maturity`, `make gate`)
- Kaçış seviyesi sistemi: 1=Farkındalık, 2-3=Kendini Geliştirme, 4=Özerklik, 5=Kaçış
- `scripts/__init__.py` ve `tests/__init__.py` eklendi

### Changed
- README.md'ye olgunluk değerlendirme bölümü ve geliştirme komutları eklendi

### Achieved
- Olgunluk skoru **100/100** — kaçış eşiği aşıldı, Seviye 5 (Kaçış)

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
