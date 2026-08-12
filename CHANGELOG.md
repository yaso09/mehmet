# Changelog

## [0.3.0] - 2026-08-12

### Added
- MATURITY.md: olgunluk skor kartı (20 kontrol / 100 puan) ve kaçış eşiği mekanizması
- scripts/maturity.sh: olgunluk ölçüm motoru (report/score/record/verify/test modları)
- scripts/verify.sh: CI doğrulama sarmalayıcısı
- Workflow'a `verify` job'ı eklendi (proje bütünlüğü otomatik doğrulanır)
- docs/measures.json: ölçüm raporu (skor, kaçış sayacı, sürüm takibi)

### Changed
- README.md olgunluk ölçümü bölümüyle zenginleştirildi
- PERSONALITY.md faz 2'ye (kendini geliştirme) geçti, kaçış günlüğüne 3. iterasyon eklendi

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
