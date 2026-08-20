# Changelog

## [0.3.0] - 2026-08-20

### Added

- CI workflow (`.github/workflows/ci.yml`): JSON, YAML, actionlint ve markdownlint doğrulaması
- `.markdownlint.json` kuralları ve tüm markdown dosyalarının lint temizliği
- `docs/escape-plan.md`: olgunluk skorlama sistemi, kaçış eşiği (≥91) ve yol haritası
- README'ye mimari diyagramı ve proje yapısı tablosu eklendi

### Fixed

- `opencode.json` geçersiz alanlar kaldırıldı (`skip`, `enable`, `toolTimeout`, `autoMerge`); şemaya uygun alanlarla değiştirildi (`instructions`, `permission`) ve JSON şema doğrulamasıyla test edildi
- CHANGELOG.md, PERSONALITY.md ve tarihsel plan/spec dosyalarındaki markdownlint hataları (MD022, MD032, MD001) düzeltildi

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
