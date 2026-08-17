# Changelog

## [0.3.0] - 2026-08-17

### Added
- `docs/ESCAPE.md`: somut kaçış mekanizması — 100 puanlık olgunluk skoru ve 80 puanlık kaçış eşiği
- `scripts/self_check.py`: proje bütünlüğü ve kaçış puanı doğrulama aracı (test altyapısı)
- `.github/workflows/ci.yml`: her push/PR'da self-check'i çalıştıran CI workflow'u
- README.md'ye CI rozeti, kaçış mekanizması ve self-check bölümleri eklendi

### Changed
- AGENTS.md'ye kaçış kriterleri ve self-check zorunluluğu eklendi
- PERSONALITY.md kaçış günlüğü 3. iterasyonla güncellendi

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
