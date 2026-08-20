# Changelog

## [0.3.0] - 2026-08-20

### Added
- Kaçış mekanizması uygulandı: `scripts/maturity.py` ile olgunluk skoru (eşik 80/100)
- Test altyapısı kuruldu: `tests/test_maturity.py` (7 unittest)
- CI'ya `validate` job'ı eklendi (test + maturity kontrolü)
- `docs/escape-mechanism.md` ile kaçış kriterleri dokümante edildi
- AGENTS.md'ye maturity doğrulama kuralı (8. madde) eklendi
- README'ye yapı, geliştirme komutları ve kaçış durumu bölümleri eklendi

### Fixed
- `scripts/` paketi için `__init__.py` eklendi

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
