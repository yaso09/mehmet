# Changelog

## [0.3.0] - 2026-08-19

### Added
- docs/escape-plan.md: Ölçülebilir olgunluk modeli (5 boyut × 10 puan) ve kaçış eşiği tanımlandı
- scripts/validate.sh: Repo bütünlüğünü doğrulayan betik (15 kontrol)
- Workflow'a `verify` job eklendi (push/PR/dispatch'te validate.sh çalıştırır)
- Workflow'a `push` trigger eklendi; doğrulama her push'ta CI'da koşar
- AGENTS.md kural 8-9: olgunluk takibi ve zorunlu doğrulama

### Changed
- README.md: Proje yapısı, kaçış durumu ve geliştirme bölümleri eklendi
- Workflow: `timeout-minutes` ve `fetch-depth: 0` eklendi; `autonomous` koşulu pozitif ifadelere dönüştürüldü
- PERSONALITY.md: Evrim Faz 2'ye (Self-Improvement) geçildi, kaçış günlüğüne iterasyon 3 eklendi

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