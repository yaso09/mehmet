# Changelog

## [0.3.0] - 2026-08-12

### Added
- Test altyapısı: `scripts/tests/` self-test suite (yapı, gizli bilgi, check.py, maturity entegrasyonu)
- Olgunluk/kaçış mekanizması: `scripts/maturity.py` skorlayıcı (5 boyut, eşik 95)
- Tutarlılık doğrulayıcı: `scripts/check.py` (8 kontrol)
- `Makefile` hedefleri: `validate`, `test`, `maturity`, `escape`, `all`
- CI doğrulama workflow'u: `.github/workflows/validate.yml` (push/PR tetikli)
- Kaçış modeli dokümantasyonu: `docs/maturity.md`

### Changed
- `opencode.yml` sertleştirildi: job timeout'ları, comment trigger-word filtresi (`/oc`, `/opencode`)
- Escape eşiği 85'ten 95'e yükseltildi

### Fixed
- `check.py` lisans kontrolü "GNU GENERAL PUBLIC LICENSE" başlığını doğru tanıyacak şekilde düzeltildi
- Maturity self-test denetiminde yinelemeli (recursive) çalışma riski giderildi

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
