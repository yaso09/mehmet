# Changelog

## [0.3.0] - 2026-08-16

### Added
- `scripts/check_health.py`: Olgunluk/sağlık denetçisi — kaçış mekanizması için ölçülebilir maturity skoru (0-100) üretir
- `tests/` altyapısı: pytest ile 7 test, `scripts/check_health.py` kapsanıyor
- `pyproject.toml`: Proje metadata'sı ve pytest konfigürasyonu
- `.github/workflows/ci.yml`: Test + maturity check + YAML doğrulama otomasyonu

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
