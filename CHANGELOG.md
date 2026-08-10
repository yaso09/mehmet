# Changelog

## [0.3.0] - 2026-08-10

### Added
- `mehmet.maturity` modülü: kaçış hazırlığını ölçen 8 gösterge üzerinden puanlama sistemi, ağırlıklı skor, eşik kontrolü ve insan-okunur rapor (`python -m mehmet.maturity`)
- Pytest test altyapısı: `tests/test_maturity.py` (10 test), `pyproject.toml` (pytest config)
- CI workflow `.github/workflows/ci.yml`: her push/PR'da test çalıştırır ve maturity raporu üretir
- README'ye "Kaçış Sistemi" ve "Geliştirme" bölümleri eklendi
- .gitignore'a Python/cache kalıpları eklendi (__pycache__, .pytest_cache, .venv)

### Changed
- PERSONALITY.md'ye 3. iterasyon kaçış günlüğü eklendi; evrim aşaması Phase 2'ye taşındı

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
