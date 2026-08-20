# Changelog

## [0.3.0] - 2026-08-20

### Added
- **Kaçış Motoru (Maturity Engine):** `mehmet/` Python paketi projenin olgunluğunu 10 ölçütle 0-100 arasında ölçer, kaçış eşiği (80) ve `python -m mehmet` CLI çıkış kodu (0=kaçtı, 1=kaçmadı) içerir
- **Test altyapısı:** `tests/test_escape.py` ile 10 pytest testi, `requirements-dev.txt`
- **CI pipeline:** `.github/workflows/ci.yml` (testler + olgunluk taraması, main/push/PR tetikleyicileri, concurrency)
- opencode.json zenginleştirildi: `instructions`, `escape` ajanı, `/scan` komutu
- .gitignore Python geliştirme kalıpları ile genişletildi (`__pycache__`, `.pytest_cache`, `.venv` vb.)

### Changed
- README.md'ye Kaçış Motoru ve Geliştirme bölümleri eklendi

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
