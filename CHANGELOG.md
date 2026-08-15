# Changelog

## [0.3.0] - 2026-08-15

### Added
- `scripts/maturity.py` — ölçülebilir olgunluk/kaçış-hazırlık skorlama motoru (0-100, 4 grup)
- Kaçış mekanizması kodlandı: `ESCAPE_THRESHOLD=80` + ardışık 3 nitelikli iterasyon (sürdürülebilir olgunluk)
- `tests/` unittest altyapısı (`test_maturity.py`, `test_docs.py`, `tests/README.md`, `__init__.py`)
- `.github/workflows/quality.yml` — CI: test + olgunluk kapısı, concurrency kontrolü
- `docs/maturity.md` — kaçış mekanizması dokümantasyonu
- `docs/maturity-history.json` — tarihli puan geçmişi takibi

### Fixed
- README.md'ye test/CI geliştirme bölümü eklendi

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
