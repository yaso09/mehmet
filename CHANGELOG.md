# Changelog

## [0.3.0] - 2026-08-16

### Added
- Kaçış/olgunluk mekanizması: `scripts/score-maturity.sh` (0-100 skor, 5 faz) ve MATURITY.md
- Test altyapısı: `scripts/test.sh`, `scripts/validate.sh`, `scripts/check-links.py`
- CI workflow'u (`.github/workflows/ci.yml`) — push/PR'da test suite ve olgunluk eşiği (>= 90)
- AGENTS.md'ye somut kaçış kapısı tanımı ve iterasyon prosedürü
- README.md'ye test ve olgunluk bölümleri

### Fixed
- `opencode.json` şemasına aykırı geçersiz alanlar (`skip`, `enable`, `toolTimeout`, `autoMerge`) kaldırıldı; geçerli alanlarla yeniden yazıldı
- `scripts/validate.sh` doğrulama suite'i depo durumunu otomatik kontrol ediyor

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
