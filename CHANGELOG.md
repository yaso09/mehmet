# Changelog

## [0.3.0] - 2026-08-10

### Added
- `scripts/check_project.py` — 0-100 maturity skorlama sistemi ve `maturity.json` çıktısı
- `scripts/test_check_project.py` — stdlib unittest tabanlı doğrulama testleri
- `docs/ESCAPE_PLAN.md` — olgunluk modeli, faz eşikleri ve kaçış kriterleri
- `.github/workflows/opencode.yml`'ye `validate` job'ı — schedule/dispatch'te skoru hesaplar, raporlar, değişince commit'ler
- AGENTS.md kural 8 — her iterasyonda maturity skorunu hesapla ve yükselt

### Changed
- README.md'ye "Olgunluk / Maturity" bölümü eklendi
- PERSONALITY.md faz tanımları olgunluk puanlarıyla eşleştirildi, kaçış günlüğü satır 3 eklendi
- Design spec'teki "Gelecek Geliştirmeler" (maturity mekanizması ve ilerleme metrikleri) tamamlandı

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
