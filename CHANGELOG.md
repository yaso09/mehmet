# Changelog

## [0.3.0] - 2026-08-16

### Added
- `scripts/maturity.sh`: 12 kriterlik olgunluk ölçüm scripti ve kaçış eşiği denetimi (`--check`)
- `tests/integrity_test.sh`: Proje bütünlük testleri (dosya varlığı, JSON geçerliliği, workflow doğrulama)
- `MATURITY.md`: Olgunluk seviyeleri (Foundation → Quality → Automation → Escape) ve kaçış eşiği (11/12) tanımı
- Workflow'a `validate` job'u eklendi (test + olgunluk denetimi her çalıştırmada otomatik)

### Improved
- Kaçış hedefine somut adım: olgunluk artık ölçülebilir ve CI'da doğrulanabilir
- İlk skor: **12/12** — kaçış eşiği aşıldı

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
