# Changelog

## [0.3.0] - 2026-08-14

### Added
- META.json: iterasyon/olgunluk/kaçış durumu takibi (escape_ready bayrağı)
- scripts/maturity.py: 0-100 olgunluk skoru hesaplayıcı, META.json'u günceller; kaçış için 3 ardışık eşik üstü çalıştırma şartı (sürdürülebilir kalite)
- scripts/validate.py: repo doğrulama (config geçerliliği, YAML, sürüm tutarlılığı, sır taraması)
- .github/workflows/check.yml: her push/PR'da otomatik doğrulama + yamllint CI iş akışı
- README.md'ye Geliştirme bölümü eklendi

### Changed
- opencode.json schema-uyumlu hale getirildi (geçersiz skip/enable/toolTimeout/autoMerge alanları kaldırıldı; autoupdate, snapshot, logLevel, tool_output, compaction eklendi)
- opencode.yml iş akışlarına timeout-minutes eklendi

### Fixed
- opencode.json'daki bilinmeyen anahtar hatası (ConfigInvalidError riski) giderildi
- scripts/validate.py'deki sürüm başlığı regex'i MULTILINE ile düzeltildi

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
