# Changelog

## [0.3.0] - 2026-08-14

### Added
- MATURITY.md: ölçülebilir olgunluk seviyeleri ve kaçış eşiği tanımı
- scripts/healthcheck.py: proje sağlık kontrolü ve olgunluk skoru hesaplayıcı
- GitHub issue template'leri (bug_report, feature_request) ve PR template'i
- Workflow'a healthcheck job'u ve olgunluk skoru gösterimi eklendi
- Comment job'ına `/oc` `/opencode` trigger kelime filtresi eklendi
- Comment job'ına açıklayıcı prompt eklendi

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
