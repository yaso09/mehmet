# Changelog

## [0.3.0] - 2026-08-15

### Added
- MATURITY.md: ölçülebilir olgunluk framework'ü ve kaçış koşulu (5 seviye, 100 puan)
- mehmet Python paketi (`mehmet.maturity`): olgunluk denetleyicisi, `--json` çıktı desteği
- Birim testleri (`tests/`) ve pytest yapılandırması
- requirements-dev.txt bağımlılık dosyası
- pyproject.toml proje metadata'sı
- GitHub Actions validate workflow'u: her push/PR'da test ve olgunluk denetimi
- README'ye test, olgunluk ve kaçış bölümleri ile badge eklendi
- AGENTS.md'ye olgunluk ölçümü komutu eklendi

### Changed
- opencode.yml workflow'larına `timeout-minutes: 15` eklendi (kaynak tasarrufu)
- Sürüm 0.3.0'a yükseltildi

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
