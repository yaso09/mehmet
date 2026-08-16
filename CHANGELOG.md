# Changelog

## [0.3.0] - 2026-08-16

### Added
- `scripts/validate.py`: proje sağlığı doğrulama aracı ve kaçış olgunluk puanı
- `.github/workflows/ci.yml`: her push/PR'da otomatik sağlık doğrulaması
- `VERSION` dosyası: semver sürüm takibi ve CHANGELOG ile senkronizasyon kontrolü
- README'e "Proje Yapısı" ve "Kaçış" bölümleri eklendi

### Fixed
- `opencode.json` şemaya uygun hale getirildi: geçersiz anahtarlar
  (`skip`, `enable`, `toolTimeout`, `autoMerge`) kaldırıldı, yerine geçerli
  yapılandırma (`autoupdate`, `share`, `instructions`, `permission`,
  `tool_output`, `compaction`) eklendi. Önceki dosya opencode'un sıkı şema
  doğrulamasını geçemezdi.

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
