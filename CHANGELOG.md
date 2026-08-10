# Changelog

## [0.3.0] - 2026-08-10

### Added
- `MATURITY.md`: kaçış (escape) rubric'i — 5 puanlama boyutu (QUALITY, TESTS, DOCS, AUTOMATION, GOVERNANCE), 25 puanlık skala ve kaçış koşulu (≥20/25, her boyut ≥3)
- `scripts/verify.sh`: proje sağlığını doğrulayan ve olgunluk puanını otomatik hesaplayan script (`--update` ile MATURITY.md durum tablosunu günceller)
- `tests/test_project.sh`: proje yapısı ve içerik bütünlüğünü denetleyen test harness
- CI `quality-gate` job'u: PR ve workflow_dispatch tetikleyicilerinde `verify.sh` + test harness zorunlu

### Changed
- `.github/workflows/opencode.yml`: konfigürasyon okunabilirliği artırıldı
- Olgunluk puanı otomatik hesaplanır hale geldi (24/25 — ESCAPE: READY)

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
