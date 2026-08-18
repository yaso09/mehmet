# Changelog

## [0.3.0] - 2026-08-18

### Added
- scripts/check-repo.sh: repo bütünlük doğrulayıcı (dosya, JSON, lisans, biçim kontrolleri)
- scripts/maturity.sh: 4 boyutlu kaçış ilerleme skoru ve evrim fazı raporu
- Makefile: `make check`, `make maturity`, `make help` hedefleri
- Workflow'a `validate` job'u eklendi (her push/PR'da `make check` çalıştırır)
- README.md'ye proje yapısı ve kalite/otomasyon bölümleri eklendi

### Fixed
- docs/superpowers/plans dosyasındaki satır sonu boşlukları temizlendi
- maturity.sh skor hesaplama hatası düzeltildi

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
