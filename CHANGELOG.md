# Changelog

## [0.3.0] - 2026-08-14

### Added
- Olgunluk (maturity) validatörü: `scripts/validate.py` ile proje sağlığı 0–100 arası ölçülüyor
- Kaçış eşiği: strict modda skor < 80 ise build başarısız oluyor
- Makefile otomasyonu (`validate`, `validate-strict`, `test`, `status`, `dev`)
- `validate` CI workflow'u: push/PR'da kalite kapısı ve CHANGELOG kontrolü
- README'ye "Olgunluk Sistemi", "Proje Yapısı" ve "Geliştirme" bölümleri eklendi

### Fixed
- Validator ve test altyapısı eksikliği (escape hedefi için kritik boşluk)

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
