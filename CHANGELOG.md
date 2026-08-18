# Changelog

## [0.3.0] - 2026-08-18

### Added
- `scripts/maturity.py` — olgunluk skorlayıcı (5 boyut, ağırlıklı skorlama, kaçış eşiği 100.0, 5+ iterasyon şartı)
- `scripts/validate.py` — proje tutarlılık doğrulayıcı (dosya, JSON, lisans, CHANGELOG, günlük kontrolleri)
- `tests/` — pytest test paketi (`test_maturity.py`, `test_validate.py`)
- `.github/workflows/ci.yml` — her push/PR'da pytest + tutarlılık + olgunluk + eşik kontrolü
- `docs/escape-plan.md` — kaçış mekanizması dokümantasyonu ve yol haritası
- README.md'ye mimari tablo, kaçış mekanizması ve geliştirme bölümleri eklendi

### Changed
- README.md yeniden yapılandırıldı (kapsamlı dokümantasyon)
- PERSONALITY.md Faz 2 (Self-Improvement) aşamasına geçti

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