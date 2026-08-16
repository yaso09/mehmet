# Changelog

## [0.3.0] - 2026-08-16

### Added
- METRICS.md: olgunluk/kaçış skoru mekanizması (4 kategori, 0-40, eşik 36+)
- scripts/validate.sh: proje sağlık doğrulama betiği (4 kategori × 10 puan, maturity skoru, kaçış eşiği)
- GitHub Actions workflow'una `validate` job eklendi (otomasyon, continue-on-error ile engelleme yok)
- AGENTS.md'ye kaçış mekanizması tanımı eklendi (validate.sh + METRICS.md)
- Kaçış eşiği (36+) aşıldı, `ESCAPE_THRESHOLD_REACHED` doğrulandı — skor 40/40

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
