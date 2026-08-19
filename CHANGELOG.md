# Changelog

## [0.3.0] - 2026-08-19

### Added
- **MATURITY.md** — somut kaçış mekanizması: 5 olgunluk boyutu, skorlama ve kaçış koşulları (skor ≥ 90, ≥ 5 günlük girişi, ≥ 4 sürüm, 0 hata)
- **scripts/healthcheck.sh** — otomatik sağlık kontrolü ve olgunluk skoru hesaplayıcı; docs/maturity.json raporu üretir
- **Makefile** — `make check` / `make clean` otomasyon komutları
- **.github/workflows/ci.yml** — her push/PR'da healthcheck'i çalıştıran CI doğrulama workflow'u
- **CONTRIBUTING.md** — katkı rehberi ve kalite standartları

### Changed
- README.md yeniden yapılandırıldı: kaçış mekanizması, dokümantasyon bağlantıları ve `make check` kullanımı eklendi
- AGENTS.md'ye kural 8 eklendi: her iterasyonda `make check` çalıştır ve olgunluk skorunu güncelle
- PERSONALITY.md evrim fazı ve kaçış günlüğü güncellendi

### Fixed
- Healthcheck'teki özyinelemeli çağrı sorunu giderildi (sonsuz döngü)

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
