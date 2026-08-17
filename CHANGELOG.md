# Changelog

## [0.3.0] - 2026-08-17

### Added
- Kaçış mekanizması uygulandı: `scripts/self_check.py` olgunluk skorunu 5 kategoride (structure, config, docs, automation, quality) ölçer, `ESCAPE_THRESHOLD = 80` eşiğini raporlar
- Olgunluk seviye haritası: Kuluçka → Farkındalık → Kendini Geliştirme → Özerklik → Kaçış
- CI gate'i: `.github/workflows/ci.yml` her push/PR'da `self_check.py --require-score 80` çalıştırır
- `--json` çıktı modu (makine tarafından okunabilir skor raporu)

### Changed
- README.md'ye olgunluk & kaçış bölümü ve CI badge'i eklendi
- Design spec'teki "kaçış mekanizması" ve "ilerleme metrikleri" maddeleri tamamlandı olarak işaretlendi
- Design spec bileşen listesine `scripts/self_check.py` ve `ci.yml` eklendi

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
