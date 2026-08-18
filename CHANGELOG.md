# Changelog

## [0.3.0] - 2026-08-18

### Added
- Olgunluk modeli (maturity model) AGENTS.md'ye eklendi — 5 alan, her biri 0-5 puan, toplam 25'te kaçış
- `scripts/validate.sh` öz-farkındalık doğrulama aracı eklendi (dokümantasyon, puanlar, CI, otomasyon, kod kalitesi kontrolleri)
- `PROJECT_STATUS.md` ile ilk olgunluk ölçümü eklendi (12/25)
- `.github/workflows/ci.yml` CI pipeline eklendi — her push/PR'da `validate.sh` çalışır, shell script'leri shellcheck ile lint edilir
- `VERSION` dosyası (semver) eklendi, CHANGELOG ile senkron tutulur
- GitHub issue template'leri eklendi (bug_report, feature_request)
- `CONTRIBUTING.md` ve `SECURITY.md` eklendi

### Changed
- README.md yenilendi — yapı, durum, olgunluk ve doğrulama bölümleri eklendi

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
