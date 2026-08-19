# Changelog

## [0.3.0] - 2026-08-19

### Added
- `scripts/maturity.sh`: kaçış olgunluk skorlama aracı (kriter kontrolleri, yüzdelik skor, kaçış eşiği)
- `tests/`: test altyapısı — `run_tests.sh` çalıştırıcı + `maturity_test.sh` smoke testleri
- `.github/workflows/ci.yml`: doğrulama ve test CI job'u (shellcheck, JSON/YAML doğrulama, test koşumu, maturity raporu)
- README'ye Geliştirme bölümü (maturity/test/CI komutları)

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
