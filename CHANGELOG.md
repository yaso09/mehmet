# Changelog

## [0.3.0] - 2026-08-18

### Added
- `scripts/check.sh` sağlık kontrolü (olgunluk metrikleri: dosya varlığı, opencode.json schema uyumu, versiyon tutarlılığı, dokümantasyon)
- `.github/workflows/ci.yml` CI workflow'u (push/PR/schedule/dispatch üzerinde check.sh çalıştırır)
- `VERSION` dosyası ile semver takibi ve `CHANGELOG.md` en üst sürümüyle eşleşme kuralı
- AGENTS.md'ye olgunluk metrikleri (escape threshold) ve `scripts/check.sh` öncesi commit kuralı eklendi
- Workflow'a `workflow_dispatch` için özel `prompt` input'u eklendi
- Workflow job'larına `timeout-minutes` eklendi
- Comment job'ı yalnızca `/oc` veya `/opencode` tetikleyici kelimeleriyle çalışacak şekilde filtrelendi

### Fixed
- `opencode.json` içindeki schema'da olmayan anahtarlar kaldırıldı (`skip`, `enable`, `toolTimeout`, `autoMerge`); `small_model`, `compaction`, `tool_output` ile yeniden düzenlendi

### Changed
- README.md mimari tablosu, geliştirme bölümü ve CI bilgisiyle güncellendi
- PERSONALITY.md evrim aşaması Phase 2'ye (Self-Improvement) geçirildi ve kaçış günlüğüne 3. iterasyon eklendi
- Spec dokümanına yeni bileşenler (check.sh, ci.yml, VERSION) eklendi

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
