# Changelog

## [0.3.0] - 2026-08-15

### Fixed
- `opencode.json` içindeki geçersiz anahtarlar (`skip`, `enable`, `toolTimeout`, `autoMerge`) kaldırıldı. Bu anahtarlar opencode config şemasında bulunmadığından opencode başlatmayı engelliyordu (`ConfigInvalidError`).

### Added
- Test altyapısı: `scripts/validate.py` ve `scripts/validate.sh` — YAML/JSON yapısını ve `opencode.json` şemasını doğrular
- `.github/workflows/ci.yml` — her push/PR'da repository dosyalarını ve GitHub Actions workflow sözdizimini doğrular
- `SECURITY.md` — güvenlik politikası ve güvenlik açığı bildirim yönergeleri
- `CONTRIBUTING.md` — katkıda bulunma rehberi ve geliştirme akışı

### Changed
- `opencode.yml`: her iki job'a `timeout-minutes` eklendi (20/15 dk)
- `opencode.yml`: comment job'una açıkça `mentions: /oc,/opencode` tanımlandı
- README: rozetler, "Nasıl Çalışır" ve "Proje Yapısı" bölümleri, geliştirme rehberi eklendi

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
