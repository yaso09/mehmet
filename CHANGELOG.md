# Changelog

## [0.3.0] - 2026-08-14

### Added
- `scripts/verify.sh`: otomatik proje sağlık doğrulama scripti (dosya, JSON/YAML, doküman tutarlılığı ve maturity skoru kontrolü)
- `.github/workflows/verify.yml`: her push/PR'da doğrulamayı çalıştıran CI pipeline
- `docs/ESCAPE.md`: ölçülebilir kaçış kriterleri ve maturity skoru takibi
- `.github/ISSUE_TEMPLATE/`: bug report ve feature request şablonları
- `.github/pull_request_template.md`: PR şablonu
- `CONTRIBUTING.md`: katkı rehberi
- README'ye CI rozeti, kaçış durumu ve test bölümleri eklendi
- Ana workflow'a (opencode.yml) job timeout ve doğrulama adımı eklendi

### Fixed
- `opencode.json` içindeki geçersiz anahtarlar (skip, enable, toolTimeout, autoMerge) kaldırıldı; opencode config şemasıyla (`https://opencode.ai/config.json`) uyumlu hale getirildi
- Plan dokümanındaki Windows PowerShell komutları Linux/bash komutlarıyla değiştirildi

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
