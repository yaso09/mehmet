# Changelog

## [0.3.0] - 2026-08-10

### Added
- `docs/escape-plan.md`: Kaçış mekanizması ölçülebilir hale getirildi — 5 kategoride 100 puanlık olgunluk skoru ve kaçış eşiği (≥ 90 + kritik hata yok) tanımlandı
- `scripts/verify.py`: Proje bütünlüğü ve olgunluk skoru doğrulama betiği (`--json`, `--quiet` modları)
- Workflow'a `validate` job'u eklendi (doğrulama otomasyonu / PR gate)
- AGENTS.md'ye kural 8 eklendi: her iterasyonda `scripts/verify.py --json` çalıştır, skoru README'ye işle
- README'ye "Gelişim Durumu (Maturity)" bölümü ve doğrulama kullanımı eklendi

### Fixed
- opencode.json'daki geçersiz alanlar kaldırıldı (`skip`, `enable`, `toolTimeout`, `autoMerge` — config schema'sına uygun değil)

### Changed
- Design doc güncellendi: yeni bileşenler (escape-plan, verify.py, validate job) eklendi, tamamlanan maddeler işaretlendi

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
