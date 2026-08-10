# Changelog

## [0.3.0] - 2026-08-10

### Added
- Kaçış mekanizmasının somutlaştırılması: `ESCAPE.md` ile olgunluk skorlaması ve `>= 80/100` eşiği tanımlandı
- `scripts/verify.sh`: proje sağlık kontrolü ve olgunluk skoru hesaplayıcı (`--report`, `--help`, exit kodları)
- `scripts/test.sh`: `verify.sh` davranışlarını doğrulayan test suite (`test.sh` çalıştırılabilir)
- `.github/workflows/verify.yml`: her push/PR'da shellcheck + test suite + olgunluk doğrulaması çalıştıran CI kalite kapısı
- AGENTS.md'ye kaçış mekanizması tanımı eklendi

### Changed
- Olgunluk kriterleri: Foundation (30), Code Quality (30), Tests (20), Automation (20)

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
