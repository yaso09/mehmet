# Changelog

## [0.3.0] - 2026-08-17

### Added
- `scripts/health_check.py`: proje yapısal bütünlüğünü doğrulayan sağlık kontrolü
- `tests/health_check_test.py`: unittest tabanlı birim testler
- `VERSION` dosyası ve CHANGELOG/README ile versiyon tutarlılığı kontrolü
- `.github/workflows/healthcheck.yml`: her push/PR'da sağlık kontrolü ve testleri çalıştıran CI
- README'ye mimari (mermaid) ve geliştirme bölümleri

### Changed
- `.github/workflows/opencode.yml`: `comment` job'ı `/oc` ve `/opencode` trigger word'lerine göre filtrelendi, her iki job'a `timeout-minutes: 30` eklendi
- README sürüm rozeti ve geliştirme komutları güncellendi

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
