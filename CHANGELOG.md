# Changelog

## [0.3.0] - 2026-08-15

### Added
- Test altyapısı: `scripts/check.sh` repo sağlık kontrolü (JSON/YAML doğrulama, gerekli dosyalar, kaçış günlüğü, secret taraması)
- CI: `.github/workflows/validate.yml` her push/PR'da sağlık kontrolünü çalıştırır
- Kaçış mekanizması somutlaştırıldı: `docs/escape-mechanism.md` olgunluk metrikleri (M1-M6) ve kaçış eşiği
- README'ye proje yapısı, geliştirme ve doğrulama bölümleri eklendi

### Changed
- `opencode.yml` comment job'u yalnızca `/oc` veya `/opencode` trigger kelimelerini içeren yorumlarda çalışır
- Her iki job'a `timeout-minutes: 15` eklendi (kontrolsüz çalışmayı önler)
- Workflow'a `run-name` eklendi (çalışma adlarını netleştirir)

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
