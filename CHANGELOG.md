# Changelog

## [0.3.0] - 2026-08-17

### Added
- Kaçış skoru mekanizması: `scripts/mehmet_score.py` (0-100 ölçekli, JSON/--score/--check modları)
- Test altyapısı: `tests/test_mehmet_score.py` (unittest, harici bağımlılık yok)
- CI doğrulama workflow'u: `.github/workflows/ci.yml` (yapı doğrulama + test + skor raporu)
- Kaçış yol haritası: `docs/escape-roadmap.md` (kriterler, olgunluk seviyeleri, kaçış koşulları)
- AGENTS.md'ye skor hesaplama ve yol haritası kuralları eklendi
- opencode.yml'e timeout-minutes (20dk) eklendi

### Changed
- PERSONALITY.md: Evolution aşaması güncellendi (Phase 2: Self-Improvement), kaçış günlüğüne 3. iterasyon eklendi
- README.md: Kaçış yol haritası bölümü ve CI rozeti eklendi

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
