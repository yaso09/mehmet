# Changelog

## [0.3.0] - 2026-08-10

### Fixed
- `opencode.json`'daki şema dışı anahtarlar kaldırıldı (`skip`, `enable`, `toolTimeout`, `autoMerge`). Bu anahtarlar opencode'un konfigürasyon şemasında yok ve opencode'un başlatılmasını engelliyordu (`ConfigInvalidError`). Geçerli anahtarlarla değiştirildi (`share`, `autoupdate`).

### Added
- `scripts/validate.py`: sıfır-bağımlılık proje sağlık doğrulayıcısı ve olgunluk skorlayıcı eklendi (dosya bütünlüğü, opencode.json şema uyumu, lisans tutarlılığı, CHANGELOG/PERSONALITY formatı, workflow yapısı)
- `.github/workflows/verify.yml`: push/PR'da `validate.py` çalıştıran CI doğrulama job'ı eklendi
- `PERSONALITY.md`'ye Kaçış Mekanizması / Escape Mechanism bölümü ve somut olgunluk göstergeleri eklendi
- README.md'ye proje yapısı ve doğrulama bölümleri eklendi

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
