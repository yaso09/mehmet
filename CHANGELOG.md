# Changelog

## [0.3.0] - 2026-08-16

### Added
- `scripts/maturity.py` — ölçülebilir olgunluk skorlayıcı (0-100). Repo'yu tarar, kriterleri doğrular, `docs/maturity-report.json` raporunu yazar ve kaçış eşiğini takip eder.
- `tests/test_maturity.py` — standart kütüphane ile 8 birim testi (unittest).
- `MATURITY.md` — kaçış eşiği (≥80/100, üst üste 3 ardışık çalıştırma) ve skor kartı dokümantasyonu.
- `.github/workflows/validate.yml` — PR/push'ta test + maturity + YAML doğrulaması yapan CI job'u.
- `opencode.json` — `instructions` ve güvenli `permission` kuralları (force push, hard reset, rm -rf engellendi).

### Fixed
- `scripts/maturity.py` — `_valid_json` eksik dosyayı artık geçerli saymıyor (boş string `{}` olarak parse ediliyordu).

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
