# Changelog

## [0.3.0] - 2026-08-17

### Added
- `scripts/self-check.sh` eklendi — proje sağlık kontrolü (zorunlu dosyalar, JSON/YAML syntax, dokümantasyon bütünlüğü)
- `.github/workflows/validate.yml` eklendi — her push/PR'da `self-check` + `actionlint` çalıştıran CI doğrulama workflow'u
- PERSONALITY.md'ye **Kaçış Skoru** (Escape Score) metriği eklendi — 7/10
- AGENTS.md'ye kural 8 eklendi — değişiklik sonrası `self-check.sh` çalıştırma zorunluluğu
- README'ye badge'ler, proje yapısı ve kalite kontrol bölümleri eklendi

### Fixed
- `opencode.json` içindeki geçersiz anahtarlar (`skip`, `enable`, `toolTimeout`, `autoMerge`) kaldırıldı — bu anahtarlar schema'da yoktu ve opencode başlatılırken `ConfigInvalidError` ile sonlanıyordu. Artık schema uyumlu (`$schema`, `model`, `autoupdate`, `snapshot`)

### Changed
- `.github/workflows/opencode.yml` yorum job'ı artık yalnızca `/oc` veya `/opencode` içeren yorumlarda tetikleniyor (boşa token harcaması önlendi)

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
