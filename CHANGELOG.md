# Changelog

## [0.3.0] - 2026-08-15

### Added
- Test altyapısı: `scripts/validate.sh` doğrulama scripti (JSON, markdown, workflow, git temizliği kontrolleri)
- CI otomasyonu: `.github/workflows/validate.yml` push/PR'da doğrulamayı çalıştıran job
- PERSONALITY.md'ye ölçülebilir olgunluk skoru tablosu (60/100, kaçış eşiği 100)
- AGENTS.md'ye doğrulama ve olgunluk skoru kuralları

### Improved
- Dokümantasyon: design doc yeni bileşenlerle güncellendi
- README.md'ye doğrulama bölümü eklendi

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
