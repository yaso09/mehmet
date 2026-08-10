# Changelog

## [0.3.0] - 2026-08-10

### Added
- Test altyapısı: `scripts/validate.sh` proje sağlık kontrolü (21 kontrol: dosya varlığı, JSON/YAML geçerliliği, dokümantasyon bütünlüğü)
- Otomasyon: `.github/workflows/validate.yml` CI workflow'u (her push/PR'da sağlık kontrolü, YAML lint, shell sözdizimi)
- Maturity scorecard (olgunluk skor kartı) PERSONALITY.md'ye eklendi: 5 kategori / 50 puan, kaçış eşiği 40
- README'ye Geliştirme ve Kaçış bölümleri eklendi

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
