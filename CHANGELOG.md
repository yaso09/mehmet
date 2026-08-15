# Changelog

## [0.3.0] - 2026-08-15

### Added
- Test altyapısı eklendi (`tests/`): proje yapısını, AGENTS.md, CHANGELOG.md, README.md, PERSONALITY.md, opencode.json ve workflow'u doğrulayan 9 `unittest` testi
- Olgunluk skorlama aracı (`scripts/maturity.py`): 4 eksende (dokümantasyon, testler, otomasyon, yapı) kaçış eşiğini (80/100) ölçer
- Otomatik olgunluk raporu (`docs/maturity-report.md`) üretimi
- `Makefile` eklendi: `make test`, `make maturity`, `make verify`, `make report` hedefleri
- GitHub Actions workflow'una `test` job'ı eklendi (Python 3.12 ile integrity testleri)
- `.gitignore` genişletildi (`__pycache__/`, `*.pyc`)

### Changed
- README.md'ye "Geliştirme" bölümü eklendi (test/olgunluk araçları)

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
