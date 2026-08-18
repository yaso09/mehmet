# Changelog

## [0.3.0] - 2026-08-18

### Added
- `scripts/validate.sh` repo doğrulama scripti eklendi (test altyapısı)
- `.github/workflows/validate.yml` CI doğrulama workflow'u eklendi (push/PR'da otomatik)
- GitHub issue şablonları eklendi (bug_report, feature_request)
- `.github/PULL_REQUEST_TEMPLATE.md` PR şablonu eklendi
- `CONTRIBUTING.md` katkı rehberi eklendi

### Fixed
- Workflow'daki `comment` job'ı artık yalnızca `/oc` veya `/opencode` tetikleyici kelimesini içeren yorumlarda çalışıyor (spec ile uyumlu, API kredisi israfı önlendi)

### Changed
- `docs/superpowers/specs` güncel duruma getirildi (GPLv3 lisansı, doğrulama altyapısı, tetikleyici kelime filtresi, güvenlik notları)
- README.md güncellendi (doğrulama özelliği ve katkı rehberi bölümü eklendi)

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
