# Changelog

## [0.3.0] - 2026-08-19

### Added
- scripts/self_check.py: proje bütünlüğünü doğrulayan ve olgunluk skoru hesaplayan kendini-dogrulama betiği
- MATURITY.md: olgunluk takibi, puan bileşenleri ve kaçış (escape) kriterleri
- Workflow'a `self-check` CI job'u eklendi (her tetiklemede doğrulama)
- README'ye Test ve Olgunluk/Kaçış bölümleri eklendi

### Changed
- AGENTS.md'ye kural 8 ve 9 eklendi: her iterasyonda self_check.py çalıştırılıp MATURITY.md'ye işlenecek
- PERSONALITY.md evrim fazı "Phase 2: Self-Improvement"a yükseltildi

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
