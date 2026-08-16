# Changelog

## [0.3.0] - 2026-08-16

### Added
- `scripts/verify.py`: Proje sağlık doğrulama betiği (dosya yapısı, JSON/YAML geçerliliği, CHANGELOG ve PERSONALITY güncelliği)
- `scripts/maturity.py`: Olgunluk skoru hesabı (otomasyon, test, dokümantasyon, yapı boyutları; kaçış eşiği 80/100)
- `.github/workflows/ci.yml`: Push/PR/schedule üzerinde doğrulama ve olgunluk ölçümü yapan CI workflow'u
- `Makefile`: `verify`, `maturity`, `check` hedefleri
- `CONTRIBUTING.md`: Katkı kuralları
- `docs/README.md`: Dokümantasyon dizini
- `VERSION`: Sürüm takibi
- `tests/test_scripts.py`: Doğrulama ve olgunluk betiklerinin testleri

### Changed
- `opencode.yml`: Ajan çalışmadan önce proje sağlık ön kontrolü eklendi
- `README.md`: Proje yapısı ve geliştirme bölümü eklendi
- `scripts/verify.py` ve `scripts/maturity.py` çalıştırılabilir (executable) yapıldı

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