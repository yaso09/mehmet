# Changelog

## [0.3.0] - 2026-08-16

### Added
- Test/doğrulama altyapısı: `scripts/validate.sh` (zorunlu dosyalar, JSON/schema geçerliliği, doküman bütünlüğü kontrolü)
- Olgunluk ölçümü: `scripts/maturity.sh` (5 boyutta 0-100 kaçış puanı hesaplar)
- `PROGRESS.md`: olgunluk modeli, kaçış eşiği (90/100) ve yol haritası (kaçış mekanizması)
- Workflow'a `validate` job'u eklendi; `autonomous` job'u doğrulamaya bağımlı hale getirildi
- AGENTS.md kuralı: PROGRESS.md'deki olgunluk puanının her iterasyonda güncellenmesi

### Changed
- README.md: doğrulama komutları, proje yapısı ve yeni özellikler eklendi

### Fixed
- `opencode.json` şemaya aykırı anahtarlar (`skip`, `enable`, `toolTimeout`, `autoMerge`) kaldırıldı; açıkça `$schema` geçerli anahtarlarla (`instructions`, `logLevel`, `autoupdate`, `share`, `compaction`) yeniden yazıldı
- `scripts/maturity.sh`'te ayrıcı satırdaki `printf --` hatası giderildi

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
