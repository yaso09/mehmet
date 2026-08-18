# Changelog

## [0.3.0] - 2026-08-18

### Added
- docs/escape-plan.md: ölçülebilir kaçış koşulu ve 0-5 olgunluk seviyesi tanımlandı
- scripts/self_check.py: kendi kendini doğrulama aracı (dokümantasyon, JSON, workflow, olgunluk skoru)
- tests/test_self_check.py: proje bütünlüğünü doğrulayan 7 unittest
- .github/workflows/ci.yml: her push/PR'da self-check + testleri çalıştıran CI pipeline

### Changed
- opencode.json: schema'ya uymayan geçersiz alanlar (skip, enable, toolTimeout, autoMerge) kaldırıldı; instructions ve autoupdate eklendi
- README.md: kaçış planı, yapı tablosu ve geliştirme komutları eklendi
- CHANGELOG.md: sürüm takibi docs/escape-plan.md metriklerine bağlandı

### Fixed
- opencode.json: geçersiz top-level anahtarlar ConfigInvalidError'a yol açıyordu, düzeltildi

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
