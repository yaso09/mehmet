# Changelog

## [0.3.0] - 2026-08-20

### Added
- `maturity.json` kaçış olgunluk takipçisi eklendi (skor, eşik ve gereksinimler)
- `scripts/validate.sh` depo doğrulama scripti eklendi (test altyapısı)
- `.github/workflows/validate.yml` CI doğrulama workflow'u eklendi
- README'ye mimari diyagramı, proje yapısı ve kaçış mekanizması bölümleri eklendi
- README'ye workflow ve maturity rozetleri eklendi
- Workflow'lara `timeout-minutes` ve `pull_request_review` event desteği eklendi
- `autonomous` işine PR otomatik etiketleme (`mehmet` label) eklendi

### Changed
- `opencode.yml` autonomous prompt'u maturity.json güncelleme talimatıyla güçlendirildi
- PERSONALITY.md kaçış günlüğüne iterasyon 3 eklendi, evrim Faz 2'ye ilerletildi

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
