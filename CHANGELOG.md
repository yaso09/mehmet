# Changelog

## [0.3.0] - 2026-08-16

### Added
- `scripts/maturity.py` ile proje olgunluk skorlama sistemi eklendi (0-100, kaçış eşiği: 80)
- `tests/` altında pytest test suite eklendi (11 test)
- `requirements.txt` ve `pyproject.toml` (pytest konfigürasyonu) eklendi
- `VERSION` dosyası ile semantik versiyonlama başlatıldı
- `.github/workflows/ci.yml` eklendi — push/PR'da testleri çalıştırır ve maturity raporu üretir
- AGENTS.md'ye "Olgunluk (Maturity)" bölümü eklendi

### Changed
- README.md'ye geliştirme ve maturity kullanım talimatları eklendi

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
