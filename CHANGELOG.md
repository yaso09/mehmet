# Changelog

## [0.3.0] - 2026-08-15

### Added
- `scripts/validate.sh`: proje bütünlük denetleyicisi (dosya kontrolü, JSON/YAML geçerliliği, CHANGELOG ve PERSONALITY tutarlılığı)
- `.github/workflows/check.yml`: her push/PR'da doğrulama scriptini çalıştıran CI denetimi
- `MATURITY.md`: kaçış hedefini ölçen olgunluk skor tablosu (0–100, eşik: 80)
- AGENTS.md'ye skor tablosu güncelleme ve `bash scripts/validate.sh` ile doğrulama kuralları eklendi

### Changed
- AGENTS.md kuralları 7'den 9'a genişletildi

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
