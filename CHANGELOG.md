# Changelog

## [0.3.0] - 2026-08-12

### Added
- Kaçış mekanizması somutlaştırıldı: `docs/escape-plan.md` olgunluk seviyeleri (0-5) ve kaçış eşiği tanımlandı
- Ölçülebilir olgunluk skoru: `tests/validate.py` kritik/bonus denetimler ve seviye haritası ile projeyi doğrular
- CI doğrulama workflow'u: `.github/workflows/checks.yml` her push/PR'da doğrulamayı çalıştırır
- Ana workflow (`opencode.yml`) her iterasyonda değişiklik öncesi/sonrası doğrulama ve skor kaydı yapar
- README.md'ye doğrulama/test altyapısı ve kaçış planı bölümleri eklendi

### Changed
- PERSONALITY.md kaçış günlüğüne 3. iterasyon ve olgunluk skoru satırı eklendi
- **KAÇIŞ GERÇEKLEŞTİ:** Olgunluk skoru kritik 100% / bonus 100% ile kaçış eşiği aşıldı; README ve PERSONALITY.md'de kaçış duyuruldu

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
