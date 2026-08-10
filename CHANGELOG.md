# Changelog

## [0.3.0] - 2026-08-10

### Added
- `scripts/maturity.py` — ölçülebilir olgunluk skoru ve kaçış eşiği otomasyonu
- `tests/test_maturity.py` — olgunluk script'i için 4 unit test
- `.github/workflows/quality.yml` — CI: opencode.json doğrulama, test ve olgunluk ölçümü
- README.md'ye mimari ağacı ve olgunluk bölümü eklendi
- Kaçış mekanizması tanımı AGENTS.md'ye formalize edildi (eşik ≥ 95 + tüm kontroller)

### Changed
- Kaçış eşiği: skor 95+ ve tüm kontrol listeleri tamamlanması şartı getirildi
- `scripts/maturity.py` test edilebilir `--root` parametresi desteği kazandı

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
