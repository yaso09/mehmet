# Changelog

## [0.3.0] - 2026-08-14

### Added
- Kaçış yol haritası (docs/escape-roadmap.md): olgunluk seviyeleri L0-L4, skorlama kategorileri ve kaçış eşiği (%90)
- Geliştirici rehberi (docs/DEVELOPMENT.md): katkı kuralları, proje yapısı, komutlar
- Olgunluk skorlama betiği (scripts/check-maturity.sh): 6 kategori / 40 puan üzerinden otomatik ölçüm, `--json` CI çıktısı
- Test altyapısı (scripts/test-maturity.sh): skorlama betiğini doğrulayan 8 otomatik kontrol
- Makefile: `maturity`, `test`, `check`, `help` hedefleri
- CI olgunluk workflow'u (.github/workflows/maturity.yml): push'ta skor + testleri doğrular

### Changed
- README.md'ye Gelişim ve Kaçış bölümü eklendi
- PERSONALITY.md Phase 2'ye (Self-Improvement) ilerledi, kaçış günlüğüne 3. iterasyon eklendi

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
