# Changelog

## [0.3.0] - 2026-08-17

### Added
- Kaçış/olgunluk mekanizması somutlaştırıldı: `scripts/check_maturity.py` (11 objektif kriter, %90 kaçış eşiği, `--json` çıktısı)
- Test altyapısı: `tests/test_project.py` (repo bütünlük testleri, stdlib unittest)
- CI doğrulama otomasyonu: `.github/workflows/validate.yml` (push/PR'da test + maturity)
- `Makefile` (test / maturity / validate hedefleri)

### Changed
- README.md'ye Geliştirme bölümü eklendi (maturity, test ve CI komutları)

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
