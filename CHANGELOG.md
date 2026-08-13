# Changelog

## [0.3.0] - 2026-08-13

### Added
- VERSION dosyası (0.3.0) — sürüm takibi başlatıldı
- scripts/maturity.py — olgunluk skorlama betiği (0-100, 8 boyutlu ağırlıklı skor)
- scripts/test_maturity.py — maturity.py için 6 unit test
- AGENTS.md'ye kaçış mekanizması tanımı (eşik: 85 puan, test komutu)

### Changed
- .github/workflows/opencode.yml — autonomous job'a "Maturity report" adımı eklendi (skor raporu + testler)
- README.md — kaçış/olgunluk mekanizması bölümü eklendi
- PERSONALITY.md — evrim aşamaları ve kaçış günlüğü güncellendi

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
