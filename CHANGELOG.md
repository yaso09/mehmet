# Changelog

## [0.3.0] - 2026-08-11

### Added
- Repo sağlık testleri (`tests/test_project.py`) — zorunlu dosyalar, opencode.json şema uygunluğu, workflow YAML geçerliliği, dokümantasyon tutarlılığı
- `Makefile` — `make check` / `make test` hedefleri
- GitHub Actions `check.yml` workflow'u — her push/PR'da testleri çalıştırır
- README'ye mimari diyagramı (mermaid), geliştirme bölümü ve yol haritası eklendi

### Fixed
- `opencode.json` şema ihlali düzeltildi — geçersiz `skip`, `enable`, `toolTimeout`, `autoMerge` alanları kaldırıldı, `additionalProperties: false` nedeniyle opencode'un başlatma hatası vermesi önlendi
- `opencode.json`'a geçerli `permission` kuralları eklendi (git komutları izinli, diğerleri sorulur; son eşleşme kuralı önceliğine göre `*` başa alındı)

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
