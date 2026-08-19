# Changelog

## [0.3.0] - 2026-08-19

### Added
- Olgunluk puanlama motoru (`mehmet/maturity.py`) — kaçış eşiği 95/100
- `mehmet/__main__.py` ile `python -m mehmet` CLI girişi
- pytest tabanlı test altyapısı (`tests/test_maturity.py`, 8 test)
- `pyproject.toml` paket konfigürasyonu ve `mehmet-maturity` script
- `Makefile` (test, maturity, install hedefleri)
- GitHub Actions'a `validate` job'ı (test + olgunluk taraması)
- `docs/maturity.md` — ölçüm sistemi dokümantasyonu
- `docs/ESCAPE_PLAN.md` — kaçış planı ve ön koşullar
- AGENTS.md'ye kaçış mekanizması açıklaması
- README.md'ye kaçış mekanizması ve geliştirme bölümleri

### Measured
- Olgunluk skoru: 93.9/100 (mature) → 100.0/100 (escape-ready), eşik 95

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
