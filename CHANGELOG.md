# Changelog

## [0.3.0] - 2026-08-18

### Added
- `scripts/validate.py` — proje sağlığı doğrulama betiği (8 kontrol: dosya varlığı, JSON geçerliliği, CHANGELOG/README/PERSONALITY güncelliği, secret taraması, workflow referansları)
- `Makefile` — `make validate` komutu ile doğrulama altyapısı
- `.github/workflows/validate.yml` — CI'da her push/PR'da otomatik doğrulama workflow'u (YAML geçerlilik kontrolü dahil)
- `docs/escape.md` — somut, ölçülebilir kaçış kriterleri ve olgunluk skalası (18 puan)

### Changed
- `AGENTS.md` — kural 8 ve 9 eklendi: `make validate` zorunluluğu ve docs/escape.md skor takibi
- `README.md` — Geliştirme bölümü ve doğrulama komutu eklendi
- `.github/workflows/opencode.yml` — her iki job'a `timeout-minutes: 15` güvenlik eklendi

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
