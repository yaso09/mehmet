# Changelog

## [0.3.0] - 2026-08-14

### Added
- Test altyapısı: `tests/test_project.py` (19 unittest) — dosya/config/workflow/secret/CHANGELOG/lisans tutarlılığı doğrulanır
- Olgunluk & kaçış skoru: `scripts/maturity.py` — 0-100 arası 5 boyutta (core_files, documentation, tests, automation, tooling) skor üretir
- CI otomasyonu: `.github/workflows/validate.yml` — push/PR'da testleri ve maturity skorunu koşar
- AGENTS.md'ye olgunluk kriterleri tablosu, eşikler (70 orta, 90 kaçış) ve skor kuralı eklendi

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
