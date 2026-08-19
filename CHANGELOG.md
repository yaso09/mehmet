# Changelog

## [0.3.0] - 2026-08-19

### Added
- Test altyapısı: `scripts/validate.py` proje sağlık doğrulayıcı eklendi (JSON/YAML geçerliliği, dokümantasyon bölümleri, CHANGELOG tutarlılığı, kaçış günlüğü kontrolleri)
- CI workflow'u (`.github/workflows/ci.yml`): push/PR'da doğrulama ve whitespace kontrolü
- Issue şablonları (bug_report, feature_request) ve PR şablonu eklendi
- PERSONALITY.md'ye "Escape Readiness" (kaçış olgunluğu) metrikleri eklendi
- AGENTS.md'ye `scripts/validate.py` çalıştırma kuralı eklendi
- README.md'ye proje yapısı, geliştirme ve kurallar bölümleri eklendi

### Fixed
- opencode.json'daki schema'ya uygun olmayan alanlar (`skip`, `enable`, `toolTimeout`, `autoMerge`) kaldırıldı; config artık `https://opencode.ai/config.json` şemasına %100 uyumlu
- README.md lisans rozeti ve CI badge eklendi

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
