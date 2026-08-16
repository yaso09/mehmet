# Changelog

## [0.3.0] - 2026-08-16

### Added
- Test altyapısı: `tests/test_project.py` (stdlib unittest) — proje yapısını, konfigürasyonu, dokümantasyonu ve workflow'u otomatik doğrular
- Olgunluk ölçüm sistemi: `scripts/maturity.py` — dokümantasyon, kod kalitesi, test altyapısı ve otomasyon kategorilerinde puan verir, kaçış eşiğini (80/100) takip eder
- CI workflow'u: `.github/workflows/ci.yml` — her push/PR'de test suite ve olgunluk kontrolü çalıştırır
- README.md'ye geliştirme bölümü eklendi

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
