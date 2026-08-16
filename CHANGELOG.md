# Changelog

## [0.3.0] - 2026-08-16

### Added
- `scripts/maturity.py`: olgunluk skoru hesaplayan ve kaçış eşiğini (threshold) izleyen mekanizma eklendi
- `scripts/validate.py`: proje tutarlılığını doğrulayan script eklendi (JSON/YAML/doküman kontrolü)
- `.github/workflows/validate.yml`: push/PR'da doğrulama ve maturity ölçümü yapan CI workflow'u eklendi
- README.md'ye proje yapısı, doğrulama ve maturity bölümleri eklendi
- Design spec'teki kaçış mekanizması ve ilerleme metrikleri maddeleri tamamlandı olarak işaretlendi

### Changed
- `.github/workflows/opencode.yml`: her iki job'a `timeout-minutes: 30` eklendi

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
