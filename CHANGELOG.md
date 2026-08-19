# Changelog

## [0.3.0] - 2026-08-19

### Added
- Olgunluk değerlendirme sistemi: `scripts/assess.mjs` (bağımlılıksız, 100 puanlık model, kaçış eşiği 80) ve `npm run assess`
- Otomatik üretilen `METRICS.md` olgunluk raporu
- Test altyapısı: `package.json` + Node built-in test runner ile 10 test (`npm test`, `npm run check`, `npm run test:coverage`)
- CI workflow'u: `.github/workflows/ci.yml` (push/PR'da sözdizimi, test ve olgunluk değerlendirmesi)
- `CONTRIBUTING.md` katkı rehberi ve `SECURITY.md` güvenlik politikası
- AGENTS.md'ye olgunluk ölçümü ve `npm test` doğrulama kuralları eklendi

### Fixed
- `opencode.json` içindeki geçersiz anahtarlar kaldırıldı (`skip`, `enable`, `toolTimeout`, `autoMerge`); yalnızca `$schema` ve `model` bırakıldı

### Changed
- README.md güncellendi: olgunluk durumu, komutlar ve proje yapısı eklendi
- PERSONALITY.md güncellendi: Faz 3 (Autonomy), kaçış günlüğüne iterasyon 3 eklendi

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
