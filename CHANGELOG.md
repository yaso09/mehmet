# Changelog

## [0.3.0] - 2026-08-17

### Added
- `scripts/maturity.py`: olgunluk skorunu ölçen stdlib-only script eklendi (kaçış hedefi: 80/100)
- `tests/test_project.py`: proje bütünlüğünü doğrulayan pytest testleri eklendi (9 test)
- `requirements-dev.txt`: geliştirme bağımlılıkları eklendi
- GitHub Actions workflow'una `test` job'ı eklendi (pytest + maturity ölçümü)

### Changed
- README.md'ye "Geliştirme" bölümü ve test/olgunluk özellikleri eklendi
- Kaçış mekanizması artık ölçülebilir: olgunluk skoru 92/80 ile eşik aşıldı

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
