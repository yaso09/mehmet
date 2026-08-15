# Changelog

## [0.3.0] - 2026-08-15

### Added
- Test/doğrulama altyapısı: `scripts/validate.sh` proje sağlığını kontrol eder (dosyalar, JSON/YAML geçerliliği, dokümantasyon tutarlılığı, lint)
- `Makefile` eklendi: `validate`, `lint`, `shellcheck`, `check` hedefleri
- `.github/workflows/validate.yml`: her push/PR'da doğrulama çalıştıran CI workflow
- `METRICS.md`: olgunluk seviyesi ve kaçış skoru takibi (güncel: 36/100, L2)

### Improved
- README.md mimari diyagramı ve geliştirici araçları tablosuyla genişletildi

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
