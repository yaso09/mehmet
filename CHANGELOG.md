# Changelog

## [0.3.0] - 2026-08-12

### Added
- `scripts/maturity.py`: Olgunluk skorlama sistemi — projeyi beş kategoride puanlar, fazı belirler ve kaçış eşiğini denetler (varsayılan 85)
- `scripts/validate.py`: Proje sağlık validasyonu — zorunlu dosyalar, geçerli JSON/YAML, CHANGELOG formatı, lisans tutarlılığı ve gizli bilgi (secret) taraması
- `tests/` dizini: 18 birim testi (`test_maturity.py`, `test_validate.py`)
- `.github/workflows/ci.yml`: Push ve PR'da test + validasyon + maturity skoru çalıştıran CI pipeline
- `docs/maturity-history.json`: Skor geçmişi takibi (son 50 kayıt)
- PERSONALITY.md'ye Faz 3 (Özerklik) aşaması ve kaçış mekanizması belgelendi

### Changed
- README.md geliştirici araçları ve CI bilgisiyle güncellendi
- .gitignore'a `__pycache__/` ve `*.pyc` eklendi

### Fixed
- `scripts/maturity.py` skor hesaplaması: artık aşırı derecede yüksek skor üretmiyor, ilerleme şimdi çoklu iterasyon gerektiriyor

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
