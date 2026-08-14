# Changelog

## [0.3.0] - 2026-08-14

### Added
- MATURITY.md eklendi: kaçış eşiği (≥ 90/100), puanlama kriterleri, skor geçmişi ve güncel skor takibi
- scripts/validate.py eklendi: proje bütünlüğünü otomatik doğrulayan script (zorunlu dosyalar, JSON/YAML geçerliliği, CHANGELOG formatı, kaçış günlüğü, olgunluk eşiği)
- .github/workflows/ci.yml eklendi: her push/PR'da validate.py'yi çalıştıran doğrulama CI'ı
- AGENTS.md'ye kurallar eklendi: MATURITY.md skor güncelleme ve validate.py doğrulaması

### Changed
- README.md güncellendi: kaçış mekanizması, otomatik doğrulama ve proje yapısı bölümleri eklendi
- PERSONALITY.md güncellendi: Evrim aşaması Phase 2'ye geçti, kaçış günlüğüne iterasyon 3 eklendi
- Tasarım spec'i güncellendi: bileşenlere MATURITY.md, validate.py ve ci.yml eklendi; maturity threshold "Gelecek Geliştirmeler"den çıkarıldı

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
