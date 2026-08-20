# Changelog

## [0.3.0] - 2026-08-20

### Added
- `scripts/validate.sh` proje sağlık kontrolü (dosya bütünlüğü, JSON/YAML, içerik, lisans, git temizliği)
- `.github/workflows/check.yml` CI doğrulama workflow'u
- `MATURITY.md` olgunluk metrikleri ve kaçış eşiği takibi (36/50)
- README.md'ye yapı tablosu ve geliştirme bölümü

### Fixed
- `opencode.yml` yorum job'u artık yalnızca `/oc` veya `/opencode` ile başlayan yorumlara yanıt veriyor
- Yorum tetikleyici filtreleme, env değişkeniyle shell injection riskine karşı güvenli hale getirildi

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
