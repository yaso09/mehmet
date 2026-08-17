# Changelog

## [0.3.0] - 2026-08-17

### Added
- MATURITY.md: ölçülebilir olgunluk modeli, puanlama ölçeği ve kaçış eşiği (toplam ≥ 20/25, Test ≥ 4, Otomasyon ≥ 4, son 3 iterasyonda gerileme yok)
- scripts/validate.sh: AGENTS.md kurallarını otomatik doğrulayan script (gerekli dosyalar, geçerli JSON, changelog, kaçış günlüğü, puan tablosu, dokümantasyon tutarlılığı)
- Makefile: `validate`, `plan`, `changelog`, `check` hedefleri

### Changed
- Workflow: job'lara `timeout-minutes` eklendi (autonomous: 60dk, comment: 30dk)
- Workflow: checkout'a `fetch-depth: 0` eklendi (tam git geçmişi)
- Workflow: autonomous job'una opencode action sonrası "Kural dogrulamasi" adımı eklendi (CI'da zorunlu doğrulama)
- README.md: kaçış mekanizması, geliştirici araçları ve mimari bölümleri eklendi

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
