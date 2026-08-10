# Changelog

## [0.3.0] - 2026-08-10

### Fixed
- `opencode.json` içindeki geçersiz anahtarlar kaldırıldı (`skip`, `enable`,
  `toolTimeout`, `autoMerge`). Bu anahtarlar config schema'sında
  (`additionalProperties: false`) yasak olduğundan opencode başlatılamıyordu.
  Yerlerine geçerli ayarlar (`small_model`, `autoupdate`, `snapshot`,
  `instructions`) eklendi.

### Added
- `scripts/audit.py`: Kaçış mekanizması ve ilerleme metrikleri. Projeyi
  14 puan üzerinden denetler, `ESCAPE_THRESHOLD` (11.0) eşiğini izler ve
  raporu `.wellness` dosyasına yazar.
- Workflow'a `audit` job'ı eklendi — her çalışmada olgunluk denetimi yapılır.
- `comment` job'ına `/oc` / `/opencode` tetikleyici kelime filtresi eklendi;
  yalnızca bu komutları içeren yorumlarda çalışır.
- Design doc'a `docs/superpowers/` bölümü eklendi: `scripts/audit.py`
  bileşeni ve denetim tablosu.

### Changed
- README.md'ye "Geliştirme" bölümü eklendi (denetim betiğinin kullanımı).
- PERSONALITY.md'de kaçış günlüğüne 3. iterasyon eklendi ve Phase 1
  açıklaması ölçülebilir ilerleme metrikleriyle güncellendi.

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
