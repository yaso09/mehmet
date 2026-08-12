# Changelog

## [0.3.0] - 2026-08-12

### Added
- Test altyapısı: config, workflow ve dokümantasyonu doğrulayan unittest suite (14 test)
- `requirements.txt` (PyYAML bağımlılığı)
- CI workflow: her push/PR'de testleri otomatik çalıştıran `.github/workflows/ci.yml`
- `CONTRIBUTING.md`: katkı kuralları ve geliştirme döngüsü
- PERSONALITY.md'ye olgunluk skoru (maturity score) takip tablosu

### Changed
- README.md: CI badge, test altyapısı ve geliştirme bölümleri eklendi

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
