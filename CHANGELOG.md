# Changelog

## [0.3.0] - 2026-08-17

### Added
- `scripts/validate.py`: Yapı ve uyumluluk doğrulama (JSON/YAML, lisans, dokümantasyon bütünlüğü)
- `scripts/maturity.py`: Olgunluk skor motoru (0-100, 5 kategori) ve otomatik `docs/status.md` raporu
- `scripts/test_maturity.py`: Olgunluk motoru birim testleri (5 test)
- `Makefile`: `validate`, `maturity`, `status`, `test`, `lint`, `all` hedefleri
- `.github/workflows/validate.yml`: CI doğrulama workflow'u (validate + test + lint + maturity)
- `.yamllint`: GitHub Actions'a uygun lint konfigürasyonu

### Changed
- README.md: Olgunluk/kaçış mekanizması, geliştirme araçları ve mimari bölümleri eklendi
- README.md: `docs/status.md` otomatik üretilen rapora bağlantı eklendi

### Security
- CI workflow'ları `contents: read` ile sınırlandırıldı

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
