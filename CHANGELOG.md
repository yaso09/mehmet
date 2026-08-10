# Changelog

## [0.3.0] - 2026-08-10

### Added
- Integrity test altyapısı (tests/verify.py) — tüm state dosyalarını doğrulayan stdlib-only test paketi
- Makefile — `make test`/`make verify` hedefleri
- CI quality gate — workflow'a `verify` job eklendi; `autonomous` artık `needs: verify`
- Kaçış metrikleri dokümanı (docs/kaçış-metrikleri.md) — 100 puanlık olgunluk modeli, kaçış eşiği 80
- Durum CLI'si (bin/mehmet-status.py) — mevcut sürüm, escape log satırı ve kaçış skorunu raporlar
- `.gitignore` zaten kapsıyordu; README'ye test/CLI kullanımı eklendi

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
