# Changelog

## [0.3.0] - 2026-08-16

### Added
- **Maturity / escape mekanizması**: `scripts/maturity.py` ile proje beş boyutta (code, tests, docs, automation, config) puanlanıyor; ilerleme `docs/metrics.json`'a kaydediliyor; 80/100 eşiğinde kaçış sinyali veriliyor
- **Test altyapısı**: `tests/test_project.py` (stdlib `unittest`) ile proje bütünlüğü, lisans, changelog, config ve workflow testleri
- **CI validate job'ı**: Workflow'da `autonomous` job'ından önce testler ve maturity skoru çalıştırılıyor
- **Makefile**: `test`, `validate`, `maturity`, `docs`, `clean` hedefleri
- **Design spec**: `docs/superpowers/specs/2026-08-16-maturity-escape-mechanism.md`

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
