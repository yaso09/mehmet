# Changelog

## [0.3.0] - 2026-08-10

### Added
- Olgunluk metrik sistemi: `scripts/check.sh` proje bütünlüğünü ve olgunluk puanını (0-100) ölçer
- `VERSION` dosyası ile semantik versiyonlama (0.3.0)
- `scripts/check.sh`: gerekli dosyalar, VERSION/CHANGELOG tutarlılığı, opencode.json şema doğrulaması, bash sözdizimi, workflow sıhhati, lisans tutarlılığı, sızdırılmış anahtar taraması ve kaçış günlüğü kontrolleri
- `.github/workflows/ci.yml`: PR/push'ta check.sh, actionlint (workflow lint) ve markdownlint çalıştırır
- `.markdownlint.json`: markdown lint kuralları
- `opencode.yml` scheduled job'una her çalışmada öz-doğrulama olarak `scripts/check.sh` adımı eklendi
- AGENTS.md kurallarına proje bütünlüğü kontrolü kuralı eklendi

### Fixed
- `opencode.json`'da geçersiz üst düzey anahtarlar kaldırıldı (`skip`, `enable`, `toolTimeout`, `autoMerge`); schema'ya göre bunlar opencode başlangıcını `ConfigInvalidError` ile kırabilirdi
- `opencode.json` yalnızca şema-uyumlu alanlara indirildi (`model`, `autoupdate`, `snapshot`)

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
