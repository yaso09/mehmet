# Changelog

## [0.3.0] - 2026-08-14

### Added
- `scripts/self-check.sh` — proje tutarlılık doğrulama scripti (zorunlu dosyalar, JSON/YAML geçerliliği, CHANGELOG/PERSONALITY güncelliği, shellcheck lint)
- `.github/workflows/validate.yml` — her push ve PR'da self-check'i çalıştıran CI workflow'u
- Ana workflow'a (`opencode.yml`) her çalıştırmada ön koşul olarak self-check adımı eklendi

### Changed
- README.md'ye "Doğrulama" bölümü eklendi (test altyapısı dokümantasyonu)

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
