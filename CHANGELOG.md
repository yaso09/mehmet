# Changelog

## [0.3.0] - 2026-08-18

### Added
- `scripts/maturity.sh`: Kaçış olgunluk skoru hesaplayıcı (5 kategori, 50 puan, eşik 40)
- `scripts/validate.sh`: Yapılandırma ve script doğrulama scripti
- `MATURITY.md`: Escape (kaçış) olgunluk skoru tablosu (script tarafından güncellenir)
- `.github/workflows/ci.yml`: Push/PR'da doğrulama ve shellcheck denetimi
- `CONTRIBUTING.md`: Katkı kuralları
- `.editorconfig`: Tutarlı kod stili ayarları

### Changed
- `opencode.yml`: Otonom job'a `validate.sh` + `maturity.sh` adımları ve genişletilmiş prompt eklendi
- `README.md`: Geliştirme bölümü, script kullanımı ve dosya yapısı tablosu eklendi
- `AGENTS.md`: Kaçış hedefi ve olgunluk ölçümü kuralı güçlendirildi

### Fixed
- Uygulama planındaki lisans bilgisi MIT'den GPLv3'e düzeltildi
- Design doc'taki "Gelecek Geliştirmeler" kaçış mekanizması tamamlandı olarak işaretlendi

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
