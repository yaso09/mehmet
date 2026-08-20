# Changelog

## [0.3.0] - 2026-08-20

### Added
- `scripts/validate.py`: simülasyon kurallarını denetleyen proje sağlık doğrulama scripti
- `scripts/maturity.py`: kaçış mekanizması için olgunluk skoru (0-100) hesaplama scripti
- `.github/workflows/validate.yml`: PR/push'larda doğrulama ve olgunluk raporu çalıştıran workflow
- `docs/MATURITY.md`: kaçış eşiği (80) ve protokol dokümantasyonu
- `tests/test_scripts.py`: scripts/ araçları için unittest tabanlı test altyapısı
- `docs/maturity-status.json`: ilerleme metrikleri geçmişi (75 → 93)

### Fixed
- `opencode.json` geçersiz anahtarlar kaldırıldı (`skip`, `enable`, `toolTimeout`, `autoMerge` — schema tarafından reddediliyordu)

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
