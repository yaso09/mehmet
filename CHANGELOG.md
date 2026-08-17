# Changelog

## [0.3.0] - 2026-08-17

### Added
- Test altyapısı: `scripts/validate.sh` — zorunlu dosya, JSON/YAML ve belge bütünlüğü kontrolleri
- Olgunluk skorlama: `scripts/check-maturity.sh` — kaçış eşiğine yakınlığı 100 üzerinden ölçer (NASCENT/MATURING/ADVANCED/READY)
- `Makefile` — `make validate`, `make maturity`, `make check` hedefleri
- `.github/workflows/validate.yml` — her push ve PR'da sağlık kontrolü + olgunluk skoru çalıştıran CI

### Fixed
- `opencode.json`'daki geçersiz anahtarlar (`skip`, `enable`, `toolTimeout`, `autoMerge`) otoriter şemaya göre kaldırıldı; `instructions` eklendi
- docs/spec'teki "Gelecek Geliştirmeler" bölümü güncellendi (maturity threshold ve ilerleme metrikleri uygulandı)

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
