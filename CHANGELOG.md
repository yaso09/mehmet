# Changelog

## [0.3.0] - 2026-08-15

### Added
- Kaçış mekanizması uygulandı: `scripts/maturity.sh` olgunluk skorunu hesaplar ve `MATURITY.md`'ye yazar (100 üzerinden, eşik 80)
- Test altyapısı eklendi: `tests/run_tests.sh` yapısal bütünlüğü, içerik tutarlılığını, konfigürasyon geçerliliğini ve gizlilik taramasını doğrular
- `Makefile` eklendi: `make test`, `make maturity`, `make check` hedefleri
- AGENTS.md'ye kaçış mekanizması tanımı (eşik, ölçüm, `make check` kuralı) eklendi
- Workflow'a `timeout-minutes` ve test/olgunluk doğrulama adımı eklendi
- README.md'ye proje yapısı tablosu ve kaçış mekanizması bölümü eklendi

### Fixed
- `opencode.json` içindeki geçersiz top-level anahtarlar kaldırıldı (`skip`, `enable`, `toolTimeout`, `autoMerge`) — bu anahtarlar opencode şemasında yok ve `ConfigInvalidError`'a neden oluyordu; konfigürasyon yalnızca geçerli anahtarlara indirildi

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
