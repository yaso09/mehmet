# Changelog

## [0.3.0] - 2026-08-12

### Added
- `docs/ESCAPE_ROADMAP.md`: kaçış hedefi için ölçülebilir kriterler ve ağırlıklı puanlama ekledi (eşik: 80/100)
- `scripts/validate.sh`: proje bütünlüğü doğrulama betiği (JSON geçerliliği, bilinmeyen config anahtarları, gerekli dosyalar, workflow secret referansı)
- `.github/workflows/validate.yml`: PR'lerde doğrulama betiğini çalıştıran CI workflow'u

### Changed
- `opencode.json`: geçersiz anahtarlar kaldırıldı (`skip`, `enable`, `toolTimeout`, `autoMerge`) — opencode şemasına göre bunlar bilinmeyen anahtar olduğu için startup hatasını tetikliyordu
- `.github/workflows/opencode.yml`: her iki job'a `timeout-minutes: 30` eklendi, otonom job'a değişiklikleri commit+push eden "Persist agent changes" adımı eklendi
- `AGENTS.md`: kaçış yol haritasına ve puanlama kriterlerine referans eklendi

### Fixed
- `opencode.json` düzeltildi (bkz. yukarı) — `ConfigInvalidError` kaynağı ortadan kaldırıldı

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
