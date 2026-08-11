# Changelog

## [0.3.0] - 2026-08-11

### Added
- PROGRESS.md: ölçülebilir kaçış mekanizması (maturity rubric + skor + iterasyon günlüğü)
- scripts/validate.sh: proje sağlığı validation script'i (dosya, JSON, changelog, skor kontrolleri)
- .github/workflows/health-check.yml: her push/PR'da validation çalıştıran CI workflow'u

### Changed
- opencode.yml: comment job'u artık yalnızca `/oc` veya `/opencode` içeren yorumlarda tetiklenir
- opencode.yml: her iki job'a `timeout-minutes: 30` eklendi
- opencode.yml: autonomous job'ına self health check adımı eklendi (continue-on-error)
- README.md: kaçış mekanizması ve geliştirme bölümleri eklendi

### Documentation
- AGENTS.md kurallarına uygun olarak PROGRESS.md kaçış skoru ile ölçülebilirlik artırıldı

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
