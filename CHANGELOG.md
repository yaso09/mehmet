# Changelog

## [0.3.0] - 2026-08-12

### Added
- Olgunluk ve kaçış mekanizması: MATURITY.md (5 seviye, kaçış eşiği)
- İlerleme metrikleri: METRICS.md (iterasyon skor tablosu)
- Doğrulama altyapısı: scripts/validate_project.sh (dosya/JSON/workflow kontrolü + olgunluk skoru)
- CI workflow'u: .github/workflows/ci.yml (push/PR'de doğrulama)
- Çoklu ajan desteği: .opencode/agent/planner.md ve .opencode/agent/reviewer.md
- Skill: .opencode/skill/project-scan (tarama sürecini standartlaştırır)
- Komut: .opencode/command/validate.md (/validate)
- opencode.json'a instructions alanı eklendi

### Changed
- MATURITY.md seviye 1-4 yeşil; seviye 5 (kaçış) eşiği tanımlandı
- Design doc "Gelecek Geliştirmeler" bölümü gerçekleştirilen maddelerle güncellendi

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
