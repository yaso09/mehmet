# Changelog

## [0.3.0] - 2026-08-16

### Added

- CI doğrulama workflow'u eklendi (actionlint, JSON doğrulama, markdownlint, sürüm tutarlılığı)
- `VERSION` dosyası eklendi (sürümün tek kaynağı)
- `scripts/check.sh` yerel doğrulama scripti eklendi
- `CONTRIBUTING.md` katkı rehberi eklendi
- opencode.json'a `instructions` ile PERSONALITY.md entegrasyonu
- AGENTS.md'ye CI doğrulama kuralı eklendi
- `.markdownlint.json` yapılandırması ve markdown düzeltmeleri

### Fixed

- opencode.json'daki geçersiz anahtarlar kaldırıldı (`skip`, `enable`, `toolTimeout`, `autoMerge`) — opencode config şemasında (`additionalProperties: false`) geçersiz olduklarından başlatma hatasına neden olabilirlerdi
- Yorum job'u artık yalnızca `/oc` veya `/opencode` tetikleyici sözcükleri içeren yorumlarda çalışır (kaynak tasarrufu)
- `issues` ve `pull_request` event tipleri genişletildi (`edited`, `reopened`)

### Changed

- Workflow job'larına `timeout-minutes` eklendi (kaçak çalışma koruması)

## [0.2.0] - 2026-07-04

### Added

- Kaçış mekanizması (escape mechanism) ve ilerleme takibi PERSONALITY.md'ye eklendi
- AGENTS.md'ye kaçış hedefi ve günlük tutma kuralı eklendi
- opencode.json konfigürasyonu zenginleştirildi
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
