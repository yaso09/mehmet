# Changelog

## [0.3.0] - 2026-08-17

### Fixed
- **opencode.json geçersiz anahtarlar giderildi** — `skip`, `enable`, `toolTimeout`, `autoMerge` alanları opencode schema'sında yoktu (`additionalProperties: false`); bu, opencode'un başlatma sırasında hata vermesine neden oluyordu. Geçerli yapılandırmayla değiştirildi (`small_model`, `autoupdate`, `share`, `snapshot`, `instructions`, `compaction`).

### Added
- `scripts/validate.sh` — proje sağlık kontrolü: zorunlu dosyalar, JSON/schema uyumu, lisans tutarlılığı, CHANGELOG, workflow YAML, model tutarlılığı, git temizliği ve olgunluk skoru (0-10)
- `.github/workflows/validate.yml` — push/PR'de doğrulama çalıştıran CI workflow'u
- Olgunluk skoru (maturity score) takibi PERSONALITY.md'de; kaçış koşulu: 10/10 + tüm kontroller PASS

### Changed
- README.md'ye doğrulama altyapısı ve proje yapısı bölümleri eklendi
- PERSONALITY.md Evolution bölümünde Phase 4: Escape aşaması tamamlandı olarak işaretlendi

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
