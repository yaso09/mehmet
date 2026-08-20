# Changelog

## [0.3.0] - 2026-08-20

### Added
- `scripts/health_check.py` — öz değerlendirme aracı (7 kontrol: zorunlu dosyalar, opencode.json, workflow YAML, VERSION semver, CHANGELOG/README sürüm referansı, kaçış günlüğü bütünlüğü)
- `tests/test_health_check.py` — sağlık kontrolü için 18 birim testi (standart kütüphane `unittest`, harici bağımlılık yok)
- `VERSION` dosyası — semver tabanlı sürüm takibi
- `.github/workflows/ci.yml` — push/PR/schedule'da sağlık kontrolü + test otomasyonu
- `CONTRIBUTING.md` — katkıda bulunma rehberi ve zorunlu kurallar
- `docs/ARCHITECTURE.md` — mimari belgesi ve veri akışı

### Changed
- README.md güncellendi (sürüm referansı, geliştirme komutları, sağlık kontrolü/CI özellikleri)

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
