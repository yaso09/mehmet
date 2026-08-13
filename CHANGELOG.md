# Changelog

## [0.3.0] - 2026-08-13

### Added
- scripts/assess.py: olgunluk (maturity) değerlendirme aracı eklendi (kaçış hedefini nesnel ölçer)
- docs/MATURITY.md: olgunluk modeli ve kaçış eşiği (90/100) tanımlandı
- .github/ISSUE_TEMPLATE: bug_report ve feature_request şablonları eklendi
- .github/pull_request_template.md: PR şablonu eklendi
- Workflow'a validate job eklendi (assess.py --json + --strict)
- WORKFLOW prompt'u olgunluk puanı artırma odaklı güncellendi

### Changed
- README.md'ye Olgunluk Değerlendirmesi bölümü eklendi

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
