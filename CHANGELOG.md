# Changelog

## [0.3.0] - 2026-08-13

### Added
- scripts/validate.py — proje bütünlük doğrulayıcı (AGENTS, CHANGELOG, PERSONALITY, README/LICENSE uyumu, opencode.json, workflow)
- scripts/maturity.py — kaçış mekanizması: 4 boyutta olgunluk skoru ve kaçış eşiği (80%) takibi
- .github/workflows/validate.yml — push/PR'da validate + maturity + unit test çalıştıran CI
- tests/ — unittest tabanlı 19 test (bağımsız, ağ gerektirmez)
- README.md'ye proje yapısı ve geliştirme komutları bölümü eklendi

### Fixed
- validate.py lisans kontrolü GPLv3 LICENSE içeriğiyle uyumlu hale getirildi
- AGENTS.md kural referansı kontrolü büyük/küçük harf duyarsız yapıldı

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
