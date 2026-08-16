# Changelog

## [0.3.0] - 2026-08-16

### Added
- MATURITY.md: ölçülebilir kaçış mekanizması (6 olgunluk boyutu, kaçış eşiği, skor tablosu)
- scripts/validate.sh: repo sağlık doğrulama scripti (JSON/YAML, çakışma işaretçileri, sır taraması, sözdizimi)
- scripts/maturity-score.sh: olgunluk skorunu otomatik hesaplayan script (`--update` ile MATURITY.md günceller)
- .github/workflows/validate.yml: push/PR'da doğrulama workflow'u (validate.sh + shellcheck + maturity-score)
- README.md'ye Mimari ve Scriptler bölümleri eklendi

### Fixed
- opencode.json'daki geçersiz alanlar kaldırıldı (`skip`, `enable`, `toolTimeout`, `autoMerge`); schema ile uyumlu hale getirildi

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
