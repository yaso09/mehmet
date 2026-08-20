# Changelog

## [0.3.0] - 2026-08-20

### Added
- MATURITY.md: olgunluk matrisi ve somut kaçış kriterleri ([ESCAPE] etiketli zorunlu maddeler, skor >= 80)
- scripts/maturity.py: olgunluk skorlama aracı (rapor, `--check` format doğrulama, `--strict` kaçış koşulu zorlama)
- tests/test_maturity.py: maturity.py için 19 birim test (unittest, stdlib)
- .github/workflows/ci.yml: CI workflow (birim testler, matris doğrulama, YAML doğrulama)
- CONTRIBUTING.md: katkı rehberi
- .editorconfig: kod stili tutarlılığı
- .github/PULL_REQUEST_TEMPLATE.md ve issue template'leri (bug_report, feature_request)
- README.md: CI badge'leri, proje yapısı, geliştirme komutları ve kaçış mekanizması dokümantasyonu

### Changed
- opencode.yml workflow işlerine `timeout-minutes: 20` eklendi (kontrolsüz çalışma engelleniyor)

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
