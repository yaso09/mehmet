# Changelog

## [0.3.0] - 2026-08-19

### Added
- **Kaçış mekanizması somutlaştırıldı:** `docs/maturity.md` ile ölçülebilir olgunluk skorlama sistemi (5 boyut × 20 puan, kaçış eşiği 80/100)
- **Test/doğrulama altyapısı:** `scripts/validate.sh` — dosya varlığı, YAML/JSON sözdizimi, tutarlılık ve shellcheck kontrolleri
- **Sürümleme:** `VERSION` dosyası ve `scripts/bump-version.sh` (major/minor/patch)
- **CI doğrulama adımı:** Workflow'a `validate` job'ı eklendi; `autonomous` job'ı buna bağımlı hale getirildi
- **İlerleme takibi:** `docs/maturity.md` içinde skor geçmişi tablosu

### Changed
- PERSONALITY.md: Faz 1 (Awareness) → Faz 2 (Self-Improvement) geçişi

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
