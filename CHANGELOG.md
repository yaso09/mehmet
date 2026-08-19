# Changelog

## [0.3.0] - 2026-08-19

### Added
- `scripts/validate.sh`: proje bütünlüğünü doğrulayan script (gerekli dosyalar, JSON/YAML sözdizimi, dokümantasyon tutarlılığı, sır sızıntısı taraması)
- `.github/workflows/validate.yml`: push ve PR'larda otomatik çalışan CI doğrulama workflow'u
- README.md'ye proje yapısı ve geliştirme bölümü eklendi

### Changed
- `opencode.json` geçerli şemaya göre düzeltildi (geçersiz `skip`, `enable`, `toolTimeout`, `autoMerge` alanları kaldırıldı; `permission`, `small_model`, `instructions` eklendi)
- Ana workflow'a `timeout-minutes` ve `validate` adımı eklendi
- Schedule cron'u GitHub kuyruğu tıkanıklığını azaltmak için offsetli dakikalara (`3,13,23,33,43,53`) taşındı

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
