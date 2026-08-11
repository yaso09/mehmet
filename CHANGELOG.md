# Changelog

## [0.3.0] - 2026-08-11

### Added
- `scripts/check_project.py`: proje tutarlılık ve sağlık doğrulayıcı
- `scripts/escape_score.py`: kaçış hazırlık skoru (escape readiness) hesaplayıcı
- `Makefile`: check/score/test/docs hedefleri
- `tests/test_scripts.py`: doğrulama ve skor betikleri için unit testler
- `docs/ESCAPE.md`: kaçış planı ve olgunluk kriterleri
- CI workflow'una `Validate project` adımı eklendi (schedule/workflow_dispatch)
- README.md'ye geliştirici araçları bölümü eklendi

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
