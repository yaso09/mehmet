# Changelog

## [0.3.0] - 2026-08-20

### Added
- Maturity scoring sistemi (`scripts/maturity.py`) eklendi: 5 boyutta (docs, automation, tests, quality, resilience) 0-100 arası kaçış ilerlemesi ölçer
- Test altyapısı eklendi (`tests/`): yapı, doküman ve maturity testleri (harici bağımlılık yok)
- Sıfır-bağımlılıklı test runner (`scripts/run_tests.py`) unittest discovery ile eklendi
- `pyproject.toml` ve `Makefile` eklendi (`make test`, `make maturity`, `make check`, `make lint`)
- GitHub Actions workflow'una `quality` job eklendi: her push'ta compile check, test suite ve maturity gate (60+) çalışır
- Workflow'a `push` tetikleyicisi eklendi
- .gitignore'a Python caches (`__pycache__`, `.pytest_cache`, `*.pyc`) eklendi

### Changed
- README.md: Test/Kalite bölümü ve maturity kullanımı dokümante edildi

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
