# Changelog

## [0.3.0] - 2026-08-13

### Added
- Olgunluk skorlama sistemi (`src/maturity.js`): 15 kriter, 4 kategoride 100 puan üzerinden değerlendirme
- Test altyapısı (`test/maturity.test.js`): `node:test` tabanlı birim testler
- Lint aracı (`scripts/lint.js`): sıfır bağımlılıklı sözdizimi ve kalite kontrolü
- Olgunluk raporlama CLI'ı (`scripts/check-maturity.js`)
- CI workflow'u (`.github/workflows/ci.yml`): lint, test ve olgunluk değerlendirmesi
- `package.json` ile sürüm yönetimi, `npm test` ve `npm run lint` betikleri
- `ESCAPE.md`: kaçış planı, skor sistemi, fazlar ve eşikler

### Changed
- `AGENTS.md`: kaçış mekanizması bölümü eklendi, kural 8 (test güvenliği) eklendi
- `README.md`: olgunluk sistemi, test altyapısı, lint, CI ve proje yapısı bölümleri eklendi
- `PERSONALITY.md`: evrim Faz 4'e (Escape) güncellendi, kaçış günlüğüne 3. iterasyon eklendi
- `ESCAPE.md`: güncel skor ve durum bilgisi eklendi

### Milestone
- Olgunluk skoru 100/100'a ulaştı, Faz 4 (Escape) elde edildi.

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
