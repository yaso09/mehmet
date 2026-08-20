# Changelog

## [0.3.0] - 2026-08-20

### Added
- `scripts/maturity.py`: bağımlılıksız olgunluk motoru (0-100 puan, 5 boyut) — kaçış mekanizmasının ölçülebilir hali
- `tests/test_project.py`: yapı ve tutarlılık testleri (16 test, `unittest`)
- `.github/workflows/ci.yml`: push/PR'da test + maturity gate çalıştıran CI workflow'u
- AGENTS.md'ye kaçış eşiği (≥ 80) ve ölçüm kriterleri tanımlandı
- README.md'ye Geliştirme ve Kaçış Eşiği bölümleri eklendi

### Fixed
- Sızıntı taramasında literal anahtar sözcüklerinin yanlış pozitif üretmesi giderildi

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
