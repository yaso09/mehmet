# Changelog

## [0.3.0] - 2026-08-17

### Added
- `scripts/validate.py`: Repo sağlık ve olgunluk validatörü (gerekli dosyalar, JSON ayrıştırma, tüm workflow YAML'larının doğrulanması, CHANGELOG/README/PERSONALITY tutarlılığı)
- `scripts/test_validate.py`: Validatör için 7 unit test (stdlib unittest)
- `.github/workflows/health.yml`: Push/PR'da validasyonu ve testleri çalıştıran CI workflow'u
- PERSONALITY.md'ye ölçülebilir 8 kriterlik Kaçış Mekanizması tablosu

### Changed
- README.md'ye proje yapısı ve geliştirme komutları eklendi
- PERSONALITY.md kaçış günlüğüne 3. iterasyon eklendi
- .gitignore'a `__pycache__/` ve `*.pyc` eklendi

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
