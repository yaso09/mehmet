# Changelog

## [0.3.0] - 2026-08-12

### Added
- `scripts/maturity.py`: Olgunluk skorlama aracı (yapı, dokümantasyon, otomasyon, test altyapısı, güvenlik boyutları) ve `METRICS.md` üretimi
- `scripts/validate.sh`: Repo sağlık kontrolü (zorunlu dosyalar, JSON geçerliliği, lisans uyumu, sır sızıntısı taraması)
- GitHub Actions workflow'una `validate` job'u eklendi; her çalışmada otomatik doğrulama yapılır
- `METRICS.md`: Kaçış eşiğini izleyen nesnel ilerleme metriği dosyası
- README'ye geliştirme/doğrulama bölümü eklendi

### Changed
- Kaçış mekanizması somutlaştırıldı: olgunluk skoru 90/100 eşiğine bağlandı

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
