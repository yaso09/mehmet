# Changelog

## [0.3.0] - 2026-08-20

### Added
- Kaçış mekanizması hayata geçirildi: `mehmet/` paketi olgunluk skorlaması (0-10) yapıyor
- `python -m mehmet` ile çalışan CLI (`--json`, `--threshold` seçenekleri)
- 10 ağırlıklı kriterle proje olgunluk analizi (`mehmet/maturity.py`)
- pytest tabanlı test paketi (17 test, `tests/`)
- `pyproject.toml` ile paket yapılandırması ve `mehmet` konsol komutu
- `Makefile` (test, check, install, clean hedefleri)
- CI workflow'u (`.github/workflows/ci.yml`): push/PR'de test + olgunluk kontrolü

### Changed
- Mevcut `opencode.yml` workflow'u dokunulmadan korundu

### Fixed
- N/A

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
