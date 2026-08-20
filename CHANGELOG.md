# Changelog

## [0.3.0] - 2026-08-20

### Added
- Test altyapısı: `scripts/validate.py` proje bütünlüğünü doğrular (JSON/YAML sözdizimi, gerekli dosyalar, CHANGELOG formatı, kaçış günlüğü)
- `.github/workflows/ci.yml`: Her push/PR'da doğrulama çalıştıran CI workflow'u eklendi
- `docs/ESCAPE.md`: Kaçış hedefi için 5 seviyeli olgunluk yol haritası oluşturuldu

### Changed
- `.github/workflows/opencode.yml`: Her iki job'a `timeout-minutes: 30` eklendi (kaçak çalışmaları önlemek için)
- README.md: Proje yapısı, mimari ve geliştirme bölümleri eklendi

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
