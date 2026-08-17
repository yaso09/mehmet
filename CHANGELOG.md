# Changelog

## [0.3.0] - 2026-08-17

### Added
- `scripts/maturity.py` olgunluk skoru hesaplayıcı eklendi (10/10, kaçış eşiği 9.0)
- `tests/test_maturity.py` test altyapısı eklendi (unittest, bağımlılıksız)
- `.github/workflows/validate.yml` kalite kapısı workflow'u eklendi (test + maturity)
- `MATURITY.md` olgunluk düzeyleri ve kaçış koşulu dokümantasyonu eklendi
- `CONTRIBUTING.md` katkı kuralları eklendi
- README.md'ye proje yapısı ve maturity bölümü eklendi

### Changed
- `scripts/maturity.py` `main()` fonksiyonuna `root` parametresi eklendi (test edilebilirlik)

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
