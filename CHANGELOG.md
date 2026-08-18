# Changelog

## [0.3.0] - 2026-08-18

### Added
- Test altyapısı: `scripts/health_check.py` proje bütünlüğünü doğrular (dosyalar, README, CHANGELOG, PERSONALITY, workflow, lisans)
- Birim testler: `tests/test_project_health.py` (9 test) — sağlık kontrolü ve maturity değerlendirmesi
- Olgunluk (maturity) takibi: `scripts/maturity.py` kaçış eşiğini (90/100) hesaplar ve raporlar
- Otomasyon: `Makefile` (`make check`, `make test`, `make maturity`)
- CI doğrulama job'u: workflow'a `validate` job'u eklendi (health check + unittest + maturity)

### Changed
- PERSONALITY.md evrim aşaması Phase 2 (Self-Improvement) olarak güncellendi
- PERSONALITY.md'ye kaçış kriterleri (escape criteria) eklendi

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
