# Changelog

## [0.3.0] - 2026-08-15

### Added
- Kaçış mekanizması: `scripts/maturity.py` olgunluk değerlendirme sistemi (6 boyut, 100 puan, eşik 80)
- Test altyapısı: `tests/test_maturity.py` unittest suite (11 test)
- CI workflow: `.github/workflows/ci.yml` test + olgunluk + JSON doğrulama
- README.md'ye kaçış mekanizması ve test talimatları eklendi

### Fixed
- opencode.json'daki geçersiz anahtarlar (`skip`, `enable`, `toolTimeout`, `autoMerge`) kaldırıldı; şema uyumlu config yazıldı

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
