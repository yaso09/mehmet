# Changelog

## [0.3.0] - 2026-08-14

### Added
- `VERSION` dosyası (semver, tek kaynak sürüm bilgisi) eklendi
- `scripts/validate.sh`: proje bütünlüğü doğrulama betiği (dosya kontrolü, VERSION↔CHANGELOG uyumu, lisans, JSON geçerliliği)
- `scripts/maturity.py`: olgunluk skoru hesaplama ve kaçış mekanizması (eşik: 75/100)
- `tests/test_validate.sh`: betikler için test suite'i
- `Makefile`: ortak görevler (`make validate`, `make test`, `make maturity`, `make check`, `make ci`)
- `.github/workflows/validate.yml`: push/PR üzerinde bütünlük + test + olgunluk + shellcheck çalıştıran CI
- `docs/architecture.md`: mimari, kaçış mekanizması ve CI pipeline dokümantasyonu

### Changed
- Kaçış mekanizması `scripts/maturity.py` ile somutlaştırıldı (skor tabanlı, ölçülebilir)
- `.gitignore`'a `__pycache__/` ve `.pytest_cache/` eklenecek (Makefile clean hedefi ile uyumlu)

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
