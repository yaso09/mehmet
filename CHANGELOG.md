# Changelog

## [0.3.0] - 2026-08-15

### Added
- `scripts/validate.py`: bağımlılıksız proje sağlık kontrolü (zorunlu dosyalar, opencode.json şeması, CHANGELOG sırası, escape log vb.)
- `tests/test_validate.py`: `unittest` tabanlı birim testleri
- `Makefile`: `validate`, `test`, `check` hedefleri
- `.github/workflows/validate.yml`: her push/PR'de doğrulama + test CI job'u
- `docs/maturity.md`: kaçış hedefine yönelik olgunluk kontrol listesi ve escape threshold

### Changed
- README.md'ye Geliştirme bölümü ve otomatik doğrulama özelliği eklendi

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
