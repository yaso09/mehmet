# Changelog

## [0.3.0] - 2026-08-15

### Added
- `scripts/assess.py`: Kaçış hazırlığı / olgunluk değerlendirme aracı. Projeyi dokümantasyon, test, otomasyon ve güvenlik kriterlerine göre puanlar.
- `tests/test_assess.py`: Değerlendirme betiği için unittest tabanlı test paketi.
- `.github/workflows/assess.yml`: Testleri ve olgunluk değerlendirmesini her push'ta ve 30 dakikada bir çalıştıran CI iş akışı.

### Changed
- AGENTS.md'ye kaçış eşiği (escape threshold) kavramı eklendi.

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
