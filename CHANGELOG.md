# Changelog

## [0.3.0] - 2026-08-15

### Added
- Kaçış mekanizması hayata geçirildi: `scripts/maturity.py` altı boyutta olgunluk skoru hesaplar
- Kaçış kapısı: %100 skor gerekir ve yalnızca en az 3 farklı günde sürdürülen evrimle ulaşılır (history boyutu)
- `--json` ve `--write` seçenekleriyle makine okunur çıktı ve `MATURITY.md` raporu
- `scripts/validate.py` proje sağlık kontrolü (dosyalar, kurallar, lisans, sözdizimi)
- `.github/workflows/ci.yml` her push/PR'da doğrulama ve maturity skorunu çalıştırır
- README'ye maturity mekanizması, doğrulama ve proje yapısı bölümleri eklendi

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
