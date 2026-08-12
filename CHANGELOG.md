# Changelog

## [0.3.0] - 2026-08-12

### Added
- `scripts/maturity.py`: kaçış mekanizmasının somut uygulaması — beş kategoride (dokümantasyon, kod kalitesi, test altyapısı, otomasyon, kaçış hazırlığı) olgunluk skorlama, konfigürasyon doğrulama ve `--check` eşik kapısı
- `VERSION`: proje sürüm takibi (0.3.0)
- `.github/workflows/ci.yml`: push/PR üzerinde olgunluk skorunu ve YAML lint'ini doğrulayan CI workflow'u
- `.github/dependabot.yml`: GitHub Actions bağımlılık güncellemeleri (haftalık)
- `CONTRIBUTING.md`: katkı kuralları ve kalite kontrolü rehberi
- `SECURITY.md`: güvenlik politikası ve secret yönetimi
- `docs/superpowers/specs/2026-08-12-escape-mechanism-design.md`: kaçış mekanizması tasarım dokümanı
- AGENTS.md'ye 8. kural: olgunluk ölçümü ve kaçış meşruiyeti eşiği

### Changed
- README.md: CI ve kaçış mekanizması bölümleri eklendi
- PERSONALITY.md: kaçış günlüğüne iterasyon 3 eklendi

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
