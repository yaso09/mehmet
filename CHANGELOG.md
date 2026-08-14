# Changelog

## [0.3.0] - 2026-08-14

### Added
- Kaçış/olgunluk skorlama sistemi: `scripts/maturity.sh` (0-100, 5 boyut, `--json`/`--score`)
- Test altyapısı: `tests/test_project.sh` (bütünlük kontrolleri) ve `scripts/run-tests.sh`
- CI kalite kapısı: `.github/workflows/ci.yml` (push/PR'da testleri çalıştırır)
- Escape mechanism spec: `docs/superpowers/specs/escape-mechanism.md`
- AGENTS.md'ye kaçış mekanizması bölümü eklendi
- README.md'ye araçlar bölümü eklendi

### Fixed
- `tests/test_project.sh` içindeki `printf` seçenek hatası düzeltildi

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
