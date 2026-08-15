# Changelog

## [0.3.0] - 2026-08-15

### Added
- Ölçülebilir kaçış kriterleri tanımlandı (docs/maturity.md): 5 boyut, 100 üzerinden skorlama, kaçış eşiği (≥ 81)
- Olgunluk skorlama otomasyonu eklendi (scripts/check-maturity.py)
- Repo sağlığı test paketi eklendi (tests/test_repo_health.py, unittest)
- CI workflow'u eklendi (.github/workflows/ci.yml): test + maturity check + yamllint
- Yol haritası eklendi (docs/roadmap.md)
- yamllint yapılandırması eklendi (.yamllint)

### Changed
- AGENTS.md kaçış mekanizması artık ölçülebilir kriterlere bağlandı
- README.md'ye Geliştirme bölümü eklendi (test/maturity/lint komutları)

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
