# Changelog

## [0.3.0] - 2026-08-20

### Added
- METRICS.md olgunluk & kaçış skor kartı (100 puanlık eşik, güncel skor 95/100)
- scripts/validate.sh config doğrulama betiği (JSON, YAML, opencode.json anahtar kontrolü)
- Workflow'a "Validate config files" adımı eklendi
- CONTRIBUTING.md etkileşim ve katkı rehberi
- AGENTS.md'ye METRICS.md güncelleme kuralı (kural 8) eklendi

### Changed
- README.md proje yapısı tablosu ve geliştirme bölümüyle güncellendi
- PERSONALITY.md kaçış günlüğüne iterasyon 3 eklendi, Phase 3 (Autonomy) işaretlendi

### Fixed
- opencode.json'daki geçersiz anahtarlar kaldırıldı (skip, enable, toolTimeout, autoMerge) — şema uyumlu hale getirildi
- CHANGELOG.md 0.2.0'da belirtilen geçersiz konfigürasyon düzeltmesi

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
