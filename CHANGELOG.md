# Changelog

## [0.3.0] - 2026-08-16

### Added
- `scripts/selfcheck.py`: proje tutarlılığını doğrulayan ve kaçış (escape) skorunu %90 eşiğiyle ölçen otomatik doğrulama aracı
- `.github/workflows/ci.yml`: her push ve PR'da selfcheck'i çalıştıran kalite kontrol pipeline'ı
- `docs/ESCAPE.md`: kaçış mekanizması, metrik ve eşik dokümantasyonu
- AGENTS.md'ye kaçış mekanizması akışı eklendi (selfcheck çalıştır, skoru kaydet, başarısız kontrolleri düzelt)
- README.md'ye Geliştirme bölümü, selfcheck ve CI özellikleri eklendi

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
