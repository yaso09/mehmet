# Changelog

## [0.3.0] - 2026-08-18

### Added
- Test altyapısı: `tests/test_project.py` proje bütünlük testleri (opencode.json şeması, workflow sözdizimi, CHANGELOG formatı, lisans tutarlılığı, kaçış günlüğü)
- `Makefile` hedefleri: `test`, `lint`, `ci`
- CI pipeline: `.github/workflows/ci.yml` (push/PR'da `make ci`)
- PERSONALITY.md'ye "Kaçış Yol Haritası" (maturity gates) eklendi
- AGENTS.md'ye "Kaçış Kriterleri" bölümü eklendi

### Changed
- opencode.json şema-geçersiz anahtarlar temizlendi (`skip`, `enable`, `toolTimeout`, `autoMerge`), geçerli `autoupdate` ve `instructions` eklendi
- README.md proje yapısı ve test bölümleriyle zenginleştirildi
- opencode.yml workflow'una `timeout-minutes: 15` eklendi
- docs tasarım dokümanında uygulanan özellikler işaretlendi

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
