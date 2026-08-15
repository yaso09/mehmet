# Changelog

## [0.3.0] - 2026-08-15

### Added
- Test altyapısı: `tests/` altında stdlib `unittest` tabanlı proje bütünlüğü testleri (yapı, JSON/YAML geçerliliği, dokümantasyon, script)
- Kaçış mekanizması: `scripts/maturity.py` olgunluk skorlama aracı (yapı/dokuman/test/otomasyon/evrim kategorileri, faz eşikleri)
- `Makefile` ile `make test`, `make check`, `make maturity` komutları
- GitHub Actions'a her çalışmada test + olgunluk skoru doğrulayan `validate` job eklendi
- `CONTRIBUTING.md` ile katkı kuralları ve kalite standartları tanımlandı

### Changed
- README.md'ye geliştirme bölümü, test komutları ve olgunluk skoru açıklaması eklendi

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
