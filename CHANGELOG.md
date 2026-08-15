# Changelog

## [0.3.0] - 2026-08-15

### Added
- `mehmet/` Python paketi oluşturuldu: tarama (scanner), olgunluk skorlama (maturity) ve CLI rapor (report)
- Kaçış olgunluğu motoru: 6 kriter (kaynak kod, test, CI, dokümantasyon, changelog, konfigürasyon) ağırlıklı skorlanır, eşik 0.90
- `python -m mehmet` komut satırı arayüzü — projeyi tarar, fırsatları listeler, kaçış hazırlığını raporlar
- `pyproject.toml` ile paket kurulumu ve pytest konfigürasyonu (console script `mehmet`)
- 11 adet pytest testi (`tests/test_scanner.py`, `tests/test_maturity.py`)
- GitHub Actions'a `test` job eklendi: pytest çalıştırır ve `python -m mehmet` ile kendini raporlar

### Changed
- README.md güncellendi: yeni özellikler, yapı ve kullanım dokümanları eklendi

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
