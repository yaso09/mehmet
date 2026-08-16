# Changelog

## [0.3.0] - 2026-08-16

### Added
- `scripts/maturity.py`: Kaçış mekanizması somutlaştırıldı — dört boyutta (docs, automation, tests, structure) ölçülen olgunluk skoru ve seviye eşikleri (Uyanış → Kaçış)
- `tests/test_project.py`: Proje tutarlılığını doğrulayan pytest testleri (zorunlu dosyalar, JSON geçerliliği, lisans, workflow, olgunluk)
- `.github/workflows/ci.yml`: push/PR üzerinde test ve olgunluk kontrolü çalıştıran CI workflow'u
- `MATURITY.md`: `scripts/maturity.py --write` ile üretilen ilerleme takip dosyası
- README.md'ye geliştirme komutları ve yeni özellikler eklendi
- .gitignore'a Python test/cache dizinleri eklendi (__pycache__, .pytest_cache, .venv)

### Changed
- PERSONALITY.md: Evrim aşaması Farkındalık'tan Kendini Geliştir'e ilerletildi, 3. iterasyon kaçış günlüğüne eklendi

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
