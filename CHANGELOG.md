# Changelog

## [0.3.0] - 2026-08-19

### Added
- `scripts/validate.py`: bağımlılıksız Python 3 proje sağlık kontrolü + 100 üzerinden maturity skoru
- `.github/workflows/validate.yml`: CI workflow'u — her push ve PR'da proje bütünlüğünü doğrular
- README.md'ye Proje Yapısı ve Doğrulama bölümleri eklendi

### Changed
- `opencode.yml` comment job'u artık yalnızca `/oc` veya `/opencode` trigger kelimesi içeren yorumlarda tetiklenir (tasarım doc ile uyumlu, API kredisi tasarrufu)
- `docs/superpowers/specs`: bayat içerik güncellendi (GPLv3, güncel opencode.json, trigger kelime filtresi, tamamlanan özellikler "Gelecek Geliştirmeler"den çıkarıldı)

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
