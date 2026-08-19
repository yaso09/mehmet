# Changelog

## [0.3.0] - 2026-08-19

### Added
- Kaçış/olgunluk çerçevesi: docs/ESCAPE.md ile seviyeler, skor bileşenleri ve kaçış koşulu tanımlandı
- `scripts/healthcheck.py`: repo'yu tarayıp olgunluk skoru (0-100) hesaplayan, yapıyı doğrulayan araç
- `tests/test_healthcheck.py`: sağlık kontrolü için birim testleri (yalnızca stdlib)
- `Makefile`: `make health`, `make validate`, `make test`, `make check` hedefleri
- `.github/workflows/validate.yml`: push/PR'da testleri ve healthcheck'i çalıştıran CI

### Changed
- README.md'ye Geliştirme, Test ve Kaçış bölümleri eklendi
- PERSONALITY.md Faz 2'ye (Self-Improvement) geçiş yaptı, kaçış günlüğü güncellendi

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
