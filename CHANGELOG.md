# Changelog

## [0.3.0] - 2026-08-14

### Added
- `scripts/check_project.py` — kaçış olgunluk puanı ve sağlık kontrolü (80/100 eşiği)
- `tests/test_project.py` — proje sağlık testleri (stdlib unittest, bağımlılıksız)
- `.github/workflows/validate.yml` — PR/push/schedule üzerinde test + olgunluk kontrolü otomasyonu
- `CONTRIBUTING.md` — katkı rehberi ve kaçış kriterleri
- README.md'ye proje yapısı, doğrulama komutları ve rozetler eklendi

### Changed
- Olgunluk metrikleri artık ölçülebilir (design doc'taki "ilerleme metrikleri" hayata geçirildi)

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
