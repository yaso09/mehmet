# Changelog

## [0.3.0] - 2026-08-16

### Added
- `scripts/validate.py`: olgunluk skorlama ve doğrulama aracı (kaçış eşiği %85)
- `.github/workflows/validate.yml`: push/PR'da ve günde 4 kez çalışan CI doğrulama işi
- README.md'ye "Olgunluk ve Kaçış Durumu" bölümü
- AGENTS.md'ye her iterasyonda `scripts/validate.py` çalıştırma kuralı
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
