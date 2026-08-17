# Changelog

## [0.3.0] - 2026-08-17

### Added
- Kaçış mekanizması ölçülebilir hale getirildi: `docs/maturity.md` ile 5 kategorili olgunluk skor sistemi ve kaçış eşiği (80/100, 3 ardışık iterasyon) tanımlandı
- Test altyapısı: `scripts/check.sh` proje doğrulama betiği (dosya varlığı, JSON/YAML geçerliliği, kritik içerik kontrolü)
- CI otomasyonu: `.github/workflows/validate.yml` her push/PR'da doğrulama çalıştırır
- PERSONALITY.md'ye İlerleme Metrikleri tablosu eklendi
- README'ye proje yapısı, test komutu ve kaçış hedefi bölümleri eklendi

### Changed
- PERSONALITY.md kaçış günlüğüne iterasyon 3 eklendi

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
