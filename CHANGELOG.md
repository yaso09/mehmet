# Changelog

## [0.3.0] - 2026-08-16

### Added
- `scripts/selfcheck.sh`: repo bütünlük, sürüm tutarlılığı ve olgunluk skoru denetimi
- `VERSION` dosyası ve sürüm senkronizasyonu kontrolü (CHANGELOG/README ile)
- `Makefile` (`make check`) ile tek komutla doğrulama
- `docs/ROADMAP.md`: kaçış yol haritası ve olgunluk fazları
- GitHub Actions workflow'una `Self-check` adımı eklendi
- AGENTS.md'ye kural 8 (selfcheck zorunluluğu) ve kural 9 (VERSION senkronizasyonu)

### Fixed
- README.md'ye proje yapısı, doğrulama ve sürüm bölümleri eklendi

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
