# Changelog

## [0.3.0] - 2026-08-15

### Added
- Kaçış hazırlığını ölçen maturity skorlayıcı: `scripts/maturity.py` (0-100, PERSONALITY.md fazlarına eşlenir, CI gate olarak kullanılabilir)
- Bağımlılıksız test paketi: `tests/run.sh` (yapısal bütünlük ve config geçerliliği)
- CI doğrulama workflow'u: `.github/workflows/ci.yml` (JSON doğrulama, YAML lint, shellcheck, test + maturity koşusu)
- Katkı rehberi: `CONTRIBUTING.md`
- `VERSION` dosyası ile sürüm takibi (0.3.0)

### Changed
- Kaçış hedefi ölçülebilir hale getirildi: olgunluk skoru ≥ 90 "Escape" fazına karşılık gelir

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
