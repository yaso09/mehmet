# Changelog

## [0.3.0] - 2026-08-15

### Added
- `scripts/verify.sh` doğrulama script'i eklendi (yapı, JSON, workflow bütünlüğü, dokümantasyon tutarlılığı ve güvenlik kontrolleri)
- `.github/workflows/verify.yml` CI doğrulama workflow'u eklendi (push/PR üzerinde çalışır)
- `MATURITY.md` maturity/kaçış skor kartı eklendi (25 üzerinden skorlama, kaçış eşiği 20/25)
- AGENTS.md kuralları güncellendi: MATURITY.md bakımı ve verify.sh çalıştırma zorunluluğu
- CHANGELOG.md'ye sürüm kontrolü doğrulama kontrolü eklendi

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