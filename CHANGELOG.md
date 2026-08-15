# Changelog

## [0.3.0] - 2026-08-15

### Added
- `scripts/validate.py`: proje yapısını ve konfigürasyon dosyalarını doğrulayan araç
- `scripts/maturity.py`: olgunluk/kaçış skorunu hesaplayan araç (kaçış eşiği: %80)
- `tests/test_project.py`: 9 pytest testi (yapı, JSON, workflow, changelog, olgunluk)
- `.github/workflows/ci.yml`: push/PR'da test ve doğrulama çalıştıran CI workflow
- `requirements-dev.txt`: geliştirme bağımlılıkları (pytest, pyyaml)
- `CONTRIBUTING.md`: katkı kuralları ve geliştirme döngüsü
- `.gitignore`'a `__pycache__/` ve `.pytest_cache/` eklendi

### Changed
- README.md'ye CI ve olgunluk takibi bölümleri eklendi

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
