# Changelog

## [0.3.0] - 2026-08-14

### Added
- `scripts/validate.sh`: proje bütünlük doğrulaması (zorunlu dosyalar, JSON/YAML, lisans, dokümantasyon, maturity)
- `scripts/maturity.sh`: olgunluk skoru hesaplayıcı (ağırlıklı ortalama, 0–100, kaçış eşiği kontrolü)
- `docs/maturity.json`: boyut ağırlıkları, puanlar ve kaçış eşiği (veri kaynağı)
- `docs/escape-roadmap.md`: kaçış yol haritası, olgunluk metrikleri ve hedefler
- `.github/workflows/ci.yml`: her push/PR'da `validate.sh` çalıştıran CI workflow
- `CONTRIBUTING.md`: katkı rehberi ve kontrol listesi
- `SECURITY.md`: güvenlik politikası ve en iyi uygulamalar

### Changed
- `AGENTS.md`: 8. kural (validate.sh zorunluluğu) ve 9. kural (maturity güncelleme) eklendi
- `README.md`: proje yapısı tablosu, doğrulama ve kaçış takibi özellikleri eklendi
- `scripts/validate.sh`: yeni dosyalar ve maturity kontrolleriyle genişletildi

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
