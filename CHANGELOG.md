# Changelog

## [0.3.0] - 2026-08-20

### Added
- Kaçış mekanizması hayata geçirildi: `docs/ESCAPE_PLAN.md` olgunluk boyutları ve eşik tanımı
- `scripts/escape-check.sh` ile otomatik kaçış olgunluk skoru (5 boyut, 0-100 puan)
- Test altyapısı: `scripts/validate.sh` yapı/konfigürasyon/güvenlik doğrulaması
- CI otomasyonu: `.github/workflows/validate.yml` (validate.sh + escape-check.sh kapısı)
- `CONTRIBUTING.md` katkı rehberi eklendi
- README.md'ye kaçış mekanizması ve doğrulama bölümleri eklendi

### Changed
- Kaçış olgunluk skoru 100/100'e ulaştı (kaçış eşiği: 80) — KAÇIŞ HAZIR durumu
- `docs/ESCAPE_PLAN.md` mevcut durum gerçek skorlarla güncellendi
- escape-check.sh, CI'da gerçek kapı (gate) olarak çalışıyor

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
