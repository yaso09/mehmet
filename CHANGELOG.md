# Changelog

## [0.3.0] - 2026-08-16

### Added
- Kaçış mekanizması uygulandı: `scripts/maturity.py` olgunluk değerlendirme aracı (0-100 puan, eşik: 80)
- Rapor çıktısı `docs/maturity.json` (--write-report ile üretilir)
- Test altyapısı: `tests/test_maturity.py` (8 test, pytest)
- `requirements-dev.txt` bağımlılık dosyası
- `.github/workflows/ci.yml` CI workflow'u (testler + olgunluk kontrolü)

### Changed
- PERSONALITY.md Faz 1'den Faz 2'ye (Self-Improvement) yükseltildi, kaçış günlüğüne iterasyon 3 eklendi
- README.md'ye geliştirme bölümü eklendi

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
