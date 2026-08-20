# Changelog

## [0.3.0] - 2026-08-20

### Added
- Kaçış mekanizması uygulandı: `scripts/escape_score.py` (olgunluk skoru 0-100)
- Kaçış kriterleri: `docs/ESCAPE.md` (seviyeler, eşik, puanlama matrisi)
- Test altyapısı: `tests/` pytest testleri (escape_score + verify_project)
- Proje sağlık kontrolü: `scripts/verify_project.py`
- Otomasyon: `Makefile` (test/verify/score) ve `pyproject.toml` (pytest config)
- GitHub Actions workflow'una `verify` job'u eklendi (testler + doğrulama)

### Changed
- AGENTS.md kaçış mekanizmasını referans alacak şekilde güncellendi (kural 8-10)
- README.md'ye kaçış mekanizması ve proje yapısı bölümleri eklendi
- .gitignore Python artefaktları ile genişletildi

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
