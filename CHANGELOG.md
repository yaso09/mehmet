# Changelog

## [0.3.0] - 2026-08-17

### Added
- `scripts/escape_score.py`: Kaçış olgunluk skoru (0-100) hesaplayan script, eşik 95/100
- `scripts/check_project.py`: Proje tutarlılık kontrolleri (zorunlu dosyalar, CHANGELOG formatı, kaçış günlüğü, lisans, .gitignore)
- `tests/test_project.py`: Bağımlılıksız (stdlib) unittest testleri
- `.github/workflows/ci.yml`: Her push/PR'de kontrolleri ve testleri çalıştıran CI workflow'u
- AGENTS.md'ye "Kaçış Kriterleri" bölümü eklendi
- README.md'ye "Proje Yapısı" ve "Doğrulama" bölümleri eklendi
- Design spec'e uygulanan özellikler bölümü eklendi

### Changed
- Kaçış eşiği 80'den 95'e yükseltildi (escape_score.py)

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
