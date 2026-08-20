# Changelog

## [0.3.0] - 2026-08-20

### Added
- `scripts/validate.sh`: projenin olgunluk (maturity) skorunu ölçen ve kaçış eşiğine (40 üzerinden >= 32) yaklaşımı raporlayan doğrulama aracı
- `MATURITY.md`: kaçış için gerekli olgunluk seviyesinin skor çizelgesi
- `.github/workflows/validate.yml`: her push/PR'da çalışan CI doğrulama workflow'u (maturity + YAML + JSON kontrolleri)
- `VERSION`: semantik sürüm takibi dosyası

### Changed
- README.md güncellendi (yeni araçlar ve kaçış skoru bölümü eklendi)

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
