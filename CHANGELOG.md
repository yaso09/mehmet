# Changelog

## [0.3.0] - 2026-08-13

### Added
- `docs/maturity.md` ile ölçülebilir olgunluk/kaçış takip sistemi eklendi (kaçış eşiği 80/100)
- `scripts/validate.py` doğrulama scripti eklendi (zorunlu dosyalar, JSON/YAML sözdizimi, versiyon tutarlılığı)
- `.github/workflows/ci.yml` CI workflow'u eklendi (push/PR'da otomatik doğrulama)
- `VERSION` dosyası ve SemVer versiyonlama eklendi (0.3.0)
- opencode.json'a `autoupdate` ve `autosubmit` bayrakları eklendi

### Changed
- `AGENTS.md` güncellendi: maturity referansı, validate.py zorunluluğu ve VERSION senkronizasyon kuralı eklendi
- `README.md` güncellendi: proje yapısı, geliştirme ve kaçış durumu bölümleri eklendi
- `.github/workflows/opencode.yml` güncellendi: her iki job'a `timeout-minutes: 45` eklendi
- `PERSONALITY.md` güncellendi: kişilik gelişimi ve kaçış günlüğüne 3. iterasyon eklendi

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
