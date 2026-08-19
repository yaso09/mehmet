# Changelog

## [0.3.0] - 2026-08-19

### Added
- Test altyapısı: tests/ (19 unit test, unittest)
- Repo sağlık kontrol aracı: scripts/repo_health.py (6 kontrol: dosya varlığı, CHANGELOG formatı, opencode.json, PERSONALITY, README, secret sızıntısı)
- Workflow YAML doğrulayıcı: scripts/validate_workflows.py
- CI workflow: .github/workflows/ci.yml (test + health check + YAML doğrulama)
- Makefile: test / check / yaml / validate hedefleri
- AGENTS.md'ye doğrulama kuralı (make validate) ve olgunluk hedefi eklendi
- PERSONALITY.md'ye maturity matrisi eklendi

### Changed
- README.md güncellendi (proje yapısı, doğrulama araçları)

### Fixed
- opencode.json'daki schema'da olmayan anahtarlar (skip, enable, toolTimeout, autoMerge) kaldırıldı; geçerli alanlarla (instructions, autoupdate, logLevel, compaction) değiştirildi
- repo_health.py artık opencode.json'da schema dışı anahtarları da denetliyor (ConfigInvalidError önlemi)

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
