# Changelog

## [0.3.0] - 2026-08-17

### Added
- Kaçış eşiği artık ölçülebilir: `scripts/maturity.py` ile olgunluk skoru hesaplanıyor
- Eşik konfigürasyonu `escape.json` dosyasına taşındı (varsayılan: 80/100)
- `scripts/validate.py`: CHANGELOG/VERSION tutarlılığı ve kaçış günlüğü doğrulaması
- `VERSION` dosyası ile semantik versiyon takibi başlatıldı
- `tests/` altında unittest tabanlı test altyapısı (16 test)
- `Makefile` ile `test`, `validate`, `maturity` hedefleri
- `.github/workflows/checks.yml`: her push/PR'de test ve doğrulama çalıştıran CI
- AGENTS.md'ye somut kaçış eşiği ve metrik tanımı eklendi

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
