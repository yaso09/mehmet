# Changelog

## [0.3.0] - 2026-08-12

### Added
- `scripts/validate.sh`: proje bütünlük doğrulayıcı (dosya yapısı, JSON geçerliliği, içerik tutarlılığı)
- `scripts/maturity.sh`: olgunluk skoru ve kaçış eşiği mekanizması (ESCAPE READY @ %80)
- Workflow'a `validate` job'ı eklendi; her PR'da bütünlük ve skor otomatik doğrulanır
- `timeout-minutes` eklendi (autonomous: 15, comment: 15, validate: 5)

### Changed
- `autonomous` job'ının `if` koşulu negatif filtre yerine açık allowlist oldu (recursive tetiklenmeyi engeller)
- README.md yeniden yapılandırıldı: mimari diyagramı, bileşen tablosu ve geliştirme bölümü eklendi

### Fixed
- Workflow'da zamanaşımı (timeout) koruması yoktu; artık her job için tanımlı

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
