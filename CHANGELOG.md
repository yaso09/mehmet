# Changelog

## [0.3.0] - 2026-08-19

### Added
- `scripts/validate.sh` proje sağlık doğrulayıcı (gerekli dosyalar, JSON geçerliliği, lisans tutarlılığı, changelog ve kaçış günlüğü kontrolü)
- Workflow'a `validate` job eklendi; her çalıştırmada sağlık kontrolleri otomatik çalışır
- `autonomous` ve `comment` job'larına `timeout-minutes` eklendi (60 dk)
- PERSONALITY.md'ye Kaçış Olgunluk Matrisi eklendi (14/25, hedef 25/25)
- README'ye proje yapısı, doğrulama ve kaçış durumu bölümleri eklendi

### Fixed
- opencode.json şemaya uygun hale getirildi: geçersiz `skip`, `enable`, `toolTimeout`, `autoMerge` anahtarları kaldırıldı (schema tarafından reddediliyordu)
- opencode.json'a `default_agent`, `mehmet` ajan tanımı ve `instructions` (AGENTS.md) eklendi

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
