# Changelog

## [0.3.0] - 2026-08-19

### Added
- `scripts/verify.sh`: Repo sağlık doğrulama aracı (dosya bütünlüğü, JSON geçerliliği, sır sızıntısı kontrolü, CHANGELOG/PERSONALITY disiplini)
- `scripts/maturity.sh`: Kaçış olgunluk skoru (0-100) ve `ESCAPE_READINESS` yüzdesi hesaplayıcı — kaçış eşiği mekanizması
- `tests/smoke_test.sh`: Araçların çalıştığını doğrulayan ilk test altyapısı
- `PROGRESS.md`: Kaçış eşikleri ve metrik ağırlıklarını tanımlayan ilerleme takip dosyası
- Workflow'a "Verify repository health" adımı (verify + maturity) ve zenginleştirilmiş prompt

### Changed
- README.md'ye Araçlar ve Kaçış Mekanizması bölümleri eklendi

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
