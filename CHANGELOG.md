# Changelog

## [0.3.0] - 2026-08-18

### Added
- Kaçış mekanizması somutlaştırıldı: `MATURITY.md` olgunluk modeli ve 80/100 kaçış eşiği tanımlandı
- `scripts/validate.py` otomatik olgunluk hesaplayıcısı eklendi (4 kategori, 0-100 puan)
- GitHub Actions'a `validate` job'ı eklendi — her push/schedule/PR'da proje sağlığını doğrular
- opencode.json'a `references.docs` eklendi (agent'ın design/spec dosyalarına erişimi)

### Changed
- `.github/workflows/opencode.yml` tek akışta üç job'a ayrıldı (autonomous, validate, comment)

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
