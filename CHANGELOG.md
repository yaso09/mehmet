# Changelog

## [0.3.0] - 2026-08-16

### Added
- `scripts/check-project.sh`: proje sağlık kontrolü (zorunlu dosyalar, JSON geçerliliği, lisans tutarlılığı, `--strict` modu)
- `scripts/maturity.sh`: kaçış olgunluğu skoru (0-100) ve faz eşlemesi
- `tests/run-tests.sh`: basit bash test koşucusu
- `tests/check_project_test.sh` ve `tests/maturity_test.sh`: test durumları
- `Makefile`: check/test/maturity/ci hedefleri
- `docs/DEVELOPMENT.md`: geliştirici rehberi
- CI: workflow'a `quality` işi eklendi (her olayda `make ci` çalıştırır)
- README.md'ye geliştirme bölümü eklendi

### Changed
- `opencode.json`: `autoupdate: false` ve `share: "disabled"` eklendi (deterministik otonom davranış)

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
