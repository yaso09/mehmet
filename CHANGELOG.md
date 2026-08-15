# Changelog

## [0.3.0] - 2026-08-15

### Added
- scripts/verify.py: Kendi kendini doğrulama ve olgunluk skorlama aracı (0-100)
- MATURITY.md: Kaçış mekanizmasının somut tanımı (aşamalar, skor bileşenleri, kaçış koşulu)
- tests/test_verify.py: verify.py için unittest test paketi (12 test)
- .github/workflows/ci.yml: push/PR/schedule üzerine verify.py + test koşan CI workflow
- README.md: Self-verification ve test kullanımı dokümante edildi
- opencode.yml'ye iterasyon öncesi doğrulama adımı eklendi
- AGENTS.md kural 8: her iterasyonda verify.py ve unittest çalıştırma zorunluluğu

### Changed
- verify.py skorlama modeli: boyut bazında oransal puanlama (tam başarı = 100)

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
