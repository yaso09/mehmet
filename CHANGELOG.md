# Changelog

## [0.3.0] - 2026-08-19

### Added
- `scripts/check_project.py`: Proje sağlık kontrolü ve olgunluk (maturity) skorlaması eklendi
- `scripts/test_check_project.py`: check_project.py için 9 birim testi eklendi
- `.github/workflows/validate.yml`: Push/PR'da çalışan CI doğrulama workflow'u eklendi (sağlık kontrolü + testler)
- README.md'ye "Proje Yapısı" ve "Sağlık Kontrolü" bölümleri eklendi
- Olgunluk rubriği (14 puan) ile kaçış eşiği takibi başlatıldı

### Changed
- README.md güncellendi; yeni özellikler belgelendi

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
