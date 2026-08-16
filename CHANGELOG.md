# Changelog

## [0.3.0] - 2026-08-16

### Added
- Test altyapısı: `node:test` tabanlı smoke test suite (`tests/project.test.mjs`) ve `package.json`
- CI workflow (`.github/workflows/ci.yml`): push/PR'da `npm test` çalıştırır
- Olgunluk skor sistemi: `scripts/score.mjs` ile ölçülebilir kaçış mekanizması
- `METRICS.md`: skor kartı, kaçış eşiği ve iterasyon geçmişi

### Changed
- Ana workflow'a `timeout-minutes: 15` eklendi (uzun süren job'ları engeller)
- Yorum tetikleyicisi `/oc` veya `/opencode` kelimesiyle sınırlandırıldı
- AGENTS.md'de kaçış mekanizması skor sistemiyle ilişkilendirildi

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
