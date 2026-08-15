# Changelog

## [0.3.0] - 2026-08-15

### Added
- `src/mehmet` Python paketi eklendi (olgunluk skorlama motoru)
- `src/mehmet/maturity.py`: 4 ağırlıklı kategoride (dokümantasyon, test, kod kalitesi, otomasyon) proje olgunluğunu hesaplar
- `src/mehmet/__main__.py`: `python -m mehmet` CLI raporu ve kaçış hazırlığı kapısı
- `tests/test_maturity.py`: 10 birim testi (skorlama, ağırlıklar, kaçış eşiği)
- `Makefile`: `test`, `lint`, `maturity`, `check` görevleri
- `.editorconfig`: kod stili tutarlılığı
- `.github/workflows/ci.yml`: her push/PR'da lint + test + maturity kapısı
- `docs/ARCHITECTURE.md`: mimari dokümantasyon

### Changed
- README.md: maturity engine ve CI quality gate bölümleri eklendi
- Tasarım dokümanındaki "ilerleme metrikleri" ve "kaçış mekanizması" gelecek geliştirmeleri uygulandı

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