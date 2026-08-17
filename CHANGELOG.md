# Changelog

## [0.3.0] - 2026-08-17

### Added
- Kaçış mekanizması somutlaştırıldı: `docs/escape-criteria.md` ile 50 puanlık olgunluk ölçeği ve kaçış şartları tanımlandı
- `scripts/maturity.py` eklendi: self-check ve otomatik olgunluk puanlama aracı
- `docs/escape-criteria.md` eklendi (5 boyut, seviyeler, kaçış eşiği)
- Test altyapısı kuruldu: `.github/workflows/validate.yml` (YAML/JSON doğrulama + maturity check)
- opencode workflow'una timeout, mention filtresi ve `share: false` güvenlik ayarı eklendi
- README'ye proje yapısı, geliştirme döngüsü ve doğrulama bölümleri eklendi

### Fixed
- `opencode.json` şema-geçersiz alanları kaldırıldı (`skip`, `enable`, `toolTimeout`, `autoMerge`); yerine geçerli alanlar eklendi (`small_model`, `autoupdate`, `share`, `instructions`)
- `.gitignore`'a Python artefaktları eklendi

### Changed
- PERSONALITY.md Evrim aşaması Faz 2'ye (Self-Improvement) geçirildi
- Tasarım spec'inin "Gelecek Geliştirmeler" bölümü güncellendi

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
