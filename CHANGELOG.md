# Changelog

## [0.3.0] - 2026-08-11

### Added
- `scripts/assess.py` olgunluk değerlendirme aracı (0-100 skor, docs/maturity.md üretir)
- `tests/test_assess.py` bağımsız doğrulama testleri
- `docs/maturity.md` otomatik olgunluk raporu
- `validate.yml` CI workflow'u (opencode.json doğrulama + assess + test)
- GitHub issue template'leri (bug_report, feature_request) ve PR template'i
- `dependabot.yml` GitHub Actions bağımlılık güncellemeleri için
- AGENTS.md'ye olgunluk değerlendirme ve test kuralları (8-9)

### Fixed
- opencode.json'daki geçersiz anahtarlar kaldırıldı (`skip`, `enable`, `toolTimeout`, `autoMerge`) — schema'ya uygun hale getirildi
- README.md'ye proje yapısı, olgunluk durumu ve geliştirme komutları eklendi

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
