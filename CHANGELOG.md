# Changelog

## [0.3.0] - 2026-08-15

### Added
- `scripts/verify.sh`: Proje bütünlüğü doğrulama betiği (dosya varlığı, JSON/YAML geçerliliği, dokümantasyon tutarlılığı)
- `scripts/maturity.sh`: Kaçış hedefine yönelik olgunluk skorlama betiği (0-100)
- `.github/workflows/verify.yml`: Her push/PR'da verify.sh ve maturity.sh çalıştıran CI doğrulama workflow'u
- README.md'ye "Geliştirici Araçları" bölümü eklendi

### Changed
- Test altyapısı ve CI doğrulaması ile kaçış mekanizması güçlendirildi

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
