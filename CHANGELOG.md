# Changelog

## [0.3.0] - 2026-08-11

### Added
- `scripts/maturity.sh`: kaçış hedefini ölçülebilir kılan olgunluk skorlama sistemi (100 puan, 5 kategori, `--json` desteği)
- `MATURITY.md`: kaçış mekanizması, eşikler ve güncel skor takibi
- `Makefile`: `check`, `test`, `maturity` hedefleri
- `.github/workflows/quality.yml`: script/config doğrulama ve maturity skoru için CI gate
- README'ye Araçlar tablosu eklendi

### Fixed
- `opencode.json` geçersiz anahtarlar (`skip`, `enable`, `toolTimeout`, `autoMerge`) kaldırıldı; bu alanlar resmi şemada yok ve `ConfigInvalidError` ile açılışta hata veriyordu. Geçerli alanlarla değiştirildi (`logLevel`, `share`, `autoupdate`, `instructions`)

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
