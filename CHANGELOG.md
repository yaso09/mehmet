# Changelog

## [0.3.0] - 2026-08-18

### Added
- Kaçış/olgunluk skorlama sistemi: `docs/ESCAPE.md` + `scripts/maturity.py` (5 boyut, 100 puan, eşik 85)
- Test altyapısı: `tests/test_maturity.py` (unittest, 7 test) ve `.github/workflows/validate.yml` (push/PR doğrulama)
- CONTRIBUTING.md, SECURITY.md, .editorconfig
- Issue şablonları (bug_report, feature_request) ve PULL_REQUEST_TEMPLATE.md

### Changed
- `opencode.yml` comment job'ına `/oc` ve `/opencode` trigger-word filtresi eklendi
- README.md: Proje Yapısı, Test ve Olgunluk Skoru bölümleri eklendi
- docs/ESCAPE.md kaçış kriterleri tanımlandı

### Fixed
- `maturity.py` TODO taramasının kendi pattern'ini yanlış pozitif sayması düzeltildi
- Olgunluk boyut puanlarının toplamı 100 olacak şekilde kalibre edildi

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
