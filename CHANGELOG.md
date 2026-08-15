# Changelog

## [0.3.0] - 2026-08-15

### Added
- `scripts/verify_project.py`: Proje bütünlüğünü doğrulayan otomasyon aracı (dosya, JSON, YAML, changelog, kaçış günlüğü kontrolleri)
- `.github/workflows/verify.yml`: Her push/PR'da doğrulama aracını çalıştıran CI workflow
- `docs/maturity.md`: Olgunluk skorlama kriterleri ve kaçış koşulu (Phase 4: 50+ puan)

### Changed
- AGENTS.md kural 8 eklendi: değişikliklerden sonra `verify_project.py` çalıştırılacak
- AGENTS.md kaçış koşulu docs/maturity.md referansına bağlandı
- PERSONALITY.md Phase 2 aktif, kaçış günlüğü 3. iterasyon (skor 30) eklendi

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
