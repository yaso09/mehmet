# Changelog

## [Unreleased]

## [0.3.0] - 2026-08-19

### Added
- `scripts/self_check.py`: gerçek kod tabanı — proje kurallarını doğrulayan self-check aracı (8 kontrol: zorunlu dosyalar, CHANGELOG, README, kaçış günlüğü, opencode.json, workflow, trailing whitespace)
- `tests/test_self_check.py`: bağımlılıksız `unittest` test altyapısı (8 test)
- `.github/workflows/ci.yml`: her push/PR'da self-check + test + actionlint çalıştıran CI hattı
- `Makefile`: `make check`, `make test`, `make help` hedefleri

### Changed
- `.github/workflows/opencode.yml`: her iki job'a `timeout-minutes: 30` eklendi, schedule tetikleyicisi `main` dalına kısıtlandı
- `docs/superpowers/*`: trailing whitespace temizlendi

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
