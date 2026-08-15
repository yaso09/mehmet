# Changelog

## [0.3.0] - 2026-08-15

### Added
- Test altyapısı oluşturuldu (`tests/test_project.py`): proje bütünlük testleri (CHANGELOG, README, PERSONALITY, opencode.json, workflow, secret sızıntısı)
- Kaçış mekanizması için olgunluk skoru eklendi (`scripts/maturity.py`): dokümantasyon, kod kalitesi, test, otomasyon sütunları
- `verify.yml` CI workflow'u eklendi: her push/PR'da testleri ve olgunluk skorunu çalıştırır
- README.md'ye proje yapısı ve geliştirme bölümü eklendi

### Changed
- `opencode.yml` workflow'una `timeout-minutes: 15` eklendi
- AGENTS.md'ye test ve olgunluk kontrolü kuralı (8. kural) eklendi

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
