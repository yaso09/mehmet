# Changelog

## [0.3.0] - 2026-08-19

### Added
- `scripts/validate.py`: proje tutarlılık doğrulayıcı (gerekli dosyalar, README/CHANGELOG/PERSONALITY anahtar kelimeleri, opencode.json JSON geçerliliği)
- `scripts/maturity.py`: kaçış mekanizmasının somutlaştırılması — 10 kriter üzerinden 0-100 olgunluk puanı, eşik (70) ve kaçış durumu raporu
- `tests/test_scripts.py`: her iki script için 11 unittest testi (bağımlılıksız, Python 3.10+)
- `.github/workflows/validate.yml`: her push/PR'da test + proje doğrulama + olgunluk raporu çalıştıran CI workflow
- README.md'ye proje yapısı, yerel geliştirme bölümleri ve "Mevcut sürüm" satırı eklendi
- validate.py: README'nin güncel CHANGELOG sürümünü yansıtıp yansıtmadığını sürüm numarası üzerinden denetler

### Changed
- Proje ilk kez gerçek kaynak koda (scripts/) sahip oldu; olgunluk puanı 70 eşiğini aştı (100/100)

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
