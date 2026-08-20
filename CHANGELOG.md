# Changelog

## [0.3.0] - 2026-08-20

### Added
- `scripts/validate.sh` proje sağlık kontrolü eklendi (zorunlu dosyalar, JSON geçerliliği, yapısal tutarlılık, TODO/FIXME taraması)
- `.github/workflows/validate.yml` doğrulama CI workflow'u eklendi (push/PR'da çalışır)
- `docs/MATURITY.md` olgunluk rubriği eklendi (5 boyut, kaçış eşiği 20/25)
- PERSONALITY.md'ye `Olgunluk Takibi` bölümü ve ilk skor (18/25) eklendi
- AGENTS.md'ye doğrulama (kural 8) ve olgunluk takibi (kural 9) kuralları eklendi
- README.md'ye Olgunluk, Proje Yapısı ve Geliştirme bölümleri eklendi

### Fixed
- opencode.json'daki schema'ya uymayan alanlar kaldırıldı (`skip`, `enable`, `toolTimeout`, `autoMerge`)
- opencode.json'da geçersiz alanlar yerine `instructions` ve `compaction` kullanıldı

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
