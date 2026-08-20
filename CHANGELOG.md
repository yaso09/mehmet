# Changelog

## [0.3.0] - 2026-08-20

### Added
- Test altyapısı: `scripts/validate.sh` doğrulama betiği eklendi (JSON/YAML geçerliliği, dosya bütünlüğü, dokümantasyon tutarlılığı, opencode.json şema kontrolü)
- CI workflow'u: `.github/workflows/ci.yml` eklendi (push ve PR'da yapı doğrulaması)
- PERSONALITY.md'ye Kaçış Koşulları (escape conditions) ve olgunluk metrikleri eklendi
- README'ye proje yapısı, test bölümü ve kaçış yol haritası eklendi

### Fixed
- opencode.json düzeltildi: schema-geçersiz anahtarlar (`skip`, `enable`, `toolTimeout`, `autoMerge`) kaldırıldı; bilinmeyen top-level anahtarlar `ConfigInvalidError` ile açılmaya neden oluyordu

### Changed
- Design doc güncellendi: yeni bileşenler (ci.yml, validate.sh) eklendi, gelecek geliştirmeler bölümü yenilendi

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
