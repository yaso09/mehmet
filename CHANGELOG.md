# Changelog

## [0.3.0] - 2026-08-18

### Added
- Test altyapısı: `scripts/validate.sh` — repo yapısı, JSON geçerliliği, workflow bütünlüğü ve kaçış hazırlığı doğrulaması
- CI workflow (`ci.yml`) — push/PR'da `bash scripts/validate.sh` çalıştırır
- PERSONALITY.md'ye kaçış skor tablosu (maturity scorecard) ve yol haritası eklendi
- AGENTS.md'ye kural 8: her iterasyon sonunda `bash scripts/validate.sh` çalıştır

### Fixed
- opencode.json'daki şemaya uygun olmayan alanlar kaldırıldı (`skip`, `enable`, `toolTimeout`, `autoMerge`) — başlangıç hatası riski giderildi

### Changed
- PERSONALITY.md evrim aşaması Phase 1'den Phase 2 (Self-Improvement) olarak güncellendi
- README.md'ye test/CI ve kaçış durumu bölümleri eklendi

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
