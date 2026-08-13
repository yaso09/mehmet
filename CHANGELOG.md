# Changelog

## [0.3.0] - 2026-08-13

### Added
- `scripts/maturity.py`: maturity score hesaplayan ve kaçış eşiğini (90/100) değerlendiren otomasyon
- Faz sistemi (Phase 0-4) ve escape gate (exit code) mekanizması
- `tests/test_maturity.py`: pytest test altyapısı (6 test) ve `test_living_project_is_mature` yaşayan maturity testi
- `requirements-dev.txt`: pytest bağımlılığı
- `.github/workflows/ci.yml`: push/PR'da testleri çalıştıran CI workflow
- `docs/maturity.md`: maturity modeli ve kaçış mekanizması dokümantasyonu

### Changed
- README.md'ye kaçış mekanizması, geliştirme ve proje yapısı bölümleri eklendi
- Design spec'teki "Gelecek Geliştirmeler" bölümü uygulanan maddelerle güncellendi

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
