# Changelog

## [0.3.0] - 2026-08-17

### Added
- `scripts/validate_repo.py`: yapı, JSON/YAML, CHANGELOG formatı ve secret sızıntısı doğrulayıcısı
- `scripts/check_maturity.py`: olgunluk skoru, aşama tespiti ve markdown rapor üretici
- `tests/`: her iki script için unit testler (`unittest`)
- `.github/workflows/ci.yml`: push/PR günlük doğrulama (compileall, validation, tests, maturity)
- `.github/workflows/maintenance.yml`: günlük audit + `docs/maturity-report.md` otomatik güncelleme
- `docs/maturity.md`: olgunluk çerçevesi, aşamalar ve kaçış eşiği (3 ardışık %90+ iterasyon)
- `docs/maturity-report.md`: otomatik üretilen ilk olgunluk raporu
- AGENTS.md'ye her iterasyonda doğrulama ve olgunluk kontrolü kuralı eklendi

### Changed
- README.md: proje yapısı, geliştirme komutları ve olgunluk sistemi bölümleri eklendi
- .gitignore: `__pycache__/` ve `*.pyc` eklendi

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
