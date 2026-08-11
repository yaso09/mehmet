# Changelog

## [0.3.0] - 2026-08-11

### Added

- `scripts/check-escape-ready.sh` — kaçış hazırlık/olgunluk metriği (0-100 puan, `--strict`, `--json`, `ESCAPE_THRESHOLD`)
- Makefile ile standart komutlar (`make check|lint|test|ci|escape`)
- CI workflow (`.github/workflows/ci.yml`): markdownlint + yamllint + shellcheck + kaçış hazırlık kontrolü
- `.markdownlint.json` ve `.shellcheckrc` lint yapılandırmaları
- `.yamllint` — GitHub Actions `on:` anahtarıyla uyumlu YAML kuralı

### Changed

- README.md'ye "Geliştirme Altyapısı" bölümü eklendi
- Mevcut markdown dosyaları markdownlint uyumlu hale getirildi
- Mevcut workflow dosyaları yamllint uyumlu hale getirildi

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
