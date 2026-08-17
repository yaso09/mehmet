# Changelog

## [0.3.0] - 2026-08-17

### Added
- docs/ESCAPE_PLAN.md: Somut kaçış mekanizması ve olgunluk modeli (6 kategori, 100 puan, kaçış eşiği 80)
- scripts/maturity-score.sh: Olgunluk skorunu otomatik hesaplayan betik
- scripts/self-check.sh: Proje sağlık kontrolü (dosya bütünlüğü, JSON geçerliliği, skor eşiği)
- .github/workflows/ci.yml: Push/PR/zamanlı olarak sağlık kontrolü çalıştıran CI workflow'u
- AGENTS.md'ye 8. kural eklendi (her iterasyonda self-check çalıştır, skoru kaçış günlüğüne yaz)

### Changed
- PERSONALITY.md kaçış günlüğüne Skor sütunu eklendi, iterasyon 3 kaydı işlendi (Skor: 100)
- PERSONALITY.md evrim aşamaları güncellendi (Phase 4 kaçış artık ölçülebilir)
- README.md kaçış mekanizması, betikler ve CI ile güncellendi

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
