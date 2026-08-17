# Changelog

## [0.3.0] - 2026-08-17

### Added
- Test altyapısı: `tests/test_project.py` (proje yapısı, CHANGELOG, README, LICENSE, config, kaçış günlüğü ve maturity script doğrulaması)
- Olgunluk/kaçış ölçüm sistemi: `scripts/maturity.py` (11 metrik, 100 üzerinden skor, `--json`/`--strict` modları)
- MATURITY.md: kaçış eşiği (80/100) ve metrik tablosu
- CI workflow'u: `.github/workflows/ci.yml` (testler, olgunluk skoru, YAML doğrulama)
- README.md'ye proje yapısı ve test/olgunluk kullanım bölümleri eklendi
- AGENTS.md kural 8: kod değişikliklerinden sonra testlerin çalıştırılması

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
