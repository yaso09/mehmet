# Changelog

## [0.3.0] - 2026-08-13

### Added
- Olgunluk değerlendirme sistemi: `scripts/assess.py` (0-100 skor, 4 kategori, --record ile geçmiş kaydı)
- Yapısal doğrulama: `scripts/validate.sh` (dosya/JSON/lisans tutarlılığı)
- Stdlib-only birim testleri: `scripts/test_assess.py`
- Makefile hedefleri: assess, validate, test, check
- CI workflow: `.github/workflows/ci.yml` (PR ve dispatch tetikleyicili)
- Maturity izleme dosyası: `docs/MATURITY.md` (skor geçmişi tablosu)
- README.md'ye "Geliştirme & Olgunluk" bölümü eklendi

### Fixed
- `docs/superpowers/plans/2026-07-04-mehmet-implementation.md` içindeki MIT lisans bilgisi GPLv3 olarak düzeltildi

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
