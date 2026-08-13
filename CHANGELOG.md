# Changelog

## [0.3.0] - 2026-08-13

### Added
- `scripts/project_health.py`: somut kaçış mekanizması ölçer — 0-100 olgunluk skoru, kategori bazlı doğrulama ve JSON rapor üretimi
- `scripts/test_project_health.py`: 8 birim testi ile sağlık kontrolü doğrulaması
- `Makefile`: `test`, `health`, `score`, `json`, `clean` hedefleri
- GitHub Actions workflow'una paralel çalışan `health` job'ı (test + olgunluk kontrolü + rapor artifact)
- `.gitignore`: Python artefaktları (`__pycache__`, `*.pyc`, `.pytest_cache`, `.coverage`)

### Changed
- README.md'ye proje yapısı, geliştirme komutları ve kaçış/olgunluk mekanizması bölümleri eklendi
- PERSONALITY.md'ye kaçış günlüğü satırı ve kaçış mekanizması açıklaması eklendi

### Notes
- İlk kez ölçülen olgunluk skoru: 100/100 (eşik 80) — proje escape-ready seviyesinde

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
