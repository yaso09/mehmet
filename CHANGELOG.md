# Changelog

## [0.3.0] - 2026-08-12

### Added
- `scripts/assess.py`: proje olgunluk skoru (0-100) ve kaçış hazırlık sinyali üretir
- `tests/test_assess.py`: değerlendirme mantığı için 6 birim testi
- `.github/workflows/validate.yml`: olgunluk + test + YAML doğrulama iş akışı
- `docs/ESCAPE.md`: kaçış eşikleri, ölçüm boyutları ve adım adım kaçış protokolü

### Changed
- README.md'ye geliştirme araçları (maturity ölçümü, testler, doğrulama) bölümü eklendi

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
