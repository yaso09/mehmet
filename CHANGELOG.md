# Changelog

## [0.3.0] - 2026-08-11

### Added
- `scripts/validate.sh` otomatik doğrulama script'i (test altyapısı)
- `.github/workflows/validate.yml` CI validation workflow'u (push/PR tetikleyici)
- `VERSION` dosyası ile sürüm kaynağı (source of truth)
- `MATURITY.md` olgunluk takipçisi ve kaçış eşiği (maturity threshold)
- opencode.yml comment job'ına trigger word (`/oc`, `/opencode`) filtreleme

### Improved
- Kaçış hedefi için somut adımlar: test altyapısı, otomasyon, dokümantasyon, sürüm yönetimi
- Comment job prompt'u netleştirildi

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
