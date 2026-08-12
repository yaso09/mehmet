# Changelog

## [0.3.0] - 2026-08-12

### Added
- Kaçış mekanizması kodlandı: `src/maturity.py` ile ölçülebilir olgunluk skorlama motoru
- `ESCAPE_THRESHOLD` (8.0/10.0) ve bileşen ağırlıkları tanımlandı
- Test altyapısı: `tests/test_maturity.py` (17 unittest) ve `tests/__init__.py`
- Otomasyon: `Makefile` (test/report/strict/clean), `scripts/check_maturity.py` CLI
- `quality.yml` CI işi: her push/PR/schedule'da testleri çalıştırıp maturity raporu üretir
- `PROGRESS.md` ile iterasyon bazlı skor takibi başlatıldı
- `requirements-dev.txt` eklendi

### Changed
- PERSONALITY.md evrim aşamaları güncellendi, iki yeni kişilik özelliği (Pragmatic, Measurable) eklendi
- README.md'ye geliştirme, test ve kaçış mekanizması bölümleri eklendi
- AGENTS.md'ye kaçış mekanizması başvurusu ve test çalıştırma kuralı eklendi

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
