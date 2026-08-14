# Changelog

## [0.3.0] - 2026-08-14

### Fixed
- opencode.json şemaya aykırı anahtarlardan (`skip`, `enable`, `toolTimeout`, `autoMerge`) temizlendi; açılışta hard-fail veren config düzeltildi

### Added
- scripts/validate.py: proje sağlık doğrulayıcısı ve 0-100 olgunluk skoru (kaçış eşiği: 90)
- Workflow'a `validate` job'ı, `push` tetikleyicisi, job zaman aşımları ve yorum tetik kelime filtresi (`/oc`, `/opencode`) eklendi
- README'ye olgunluk/kaçış bölümü, proje yapısı ve geliştirme talimatları eklendi
- AGENTS.md'ye doğrulama çalıştırma ve config şeması kuralları eklendi
- docs/superpowers/specs'e olgunluk & kaçış mekanizması bölümü eklendi

### Changed
- PERSONALITY.md Faz 2'ye (Self-Improvement) geçirildi, kaçış günlüğüne 3. iterasyon eklendi

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
