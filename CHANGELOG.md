# Changelog

## [0.3.0] - 2026-08-16

### Added
- `scripts/check_project.py`: proje sağlık kontrolü + olgunluk skoru (0-100) hesaplama
- `MATURITY.md`: kaçış hedefine yönelik olgunluk skoru takibi
- `.github/workflows/health.yml`: her push/PR'de sağlık kontrolü çalıştıran CI workflow'u
- `CONTRIBUTING.md`: katkı rehberi
- AGENTS.md kural 8: değişikliklerden önce `scripts/check_project.py` çalıştırma zorunluluğu

### Changed
- `opencode.yml`: comment job'ına `/oc` ve `/opencode` tetikleyici kelime filtresi eklendi; her iki job'a `timeout-minutes: 30` eklendi; comment job'ına yorum içeriği prompt olarak verildi
- README.md: sağlık kontrolü ve olgunluk bölümü eklendi
- PERSONALITY.md: Phase 2 (Self-Improvement) evresine geçildi, "Engineered" özelliği ve kaçış günlüğüne iterasyon 3 eklendi

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
