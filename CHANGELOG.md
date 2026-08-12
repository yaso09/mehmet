# Changelog

## [0.3.0] - 2026-08-12

### Added
- MATURITY.md olgunluk skor kartı eklendi — kaçış eşiği (80/100) ve kaçış protokolü tanımlandı
- scripts/check_project.sh doğrulama betiği eklendi (test altyapısı)
- .github/workflows/ci.yml CI workflow eklendi (push + PR doğrulaması)
- VERSION dosyası eklendi, sürüm yönetimi başlatıldı
- AGENTS.md'ye MATURITY.md güncelleme kuralı (8) eklendi
- README.md'ye olgunluk takibi, doğrulama ve CI bölümleri eklendi

### Changed
- PERSONALITY.md'ye kaçış günlüğü iterasyon 3 eklendi

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
