# Changelog

## [0.3.0] - 2026-08-19

### Added
- `scripts/validate.sh`: Proje bütünlük doğrulayıcısı (dosya varlığı, JSON geçerliliği, doküman tutarlılığı)
- `scripts/maturity.sh`: Olgunluk skoru (0-100) ve kaçış seviyesi üreten ölçüm aracı
- `tests/run_tests.sh`: Pozitif ve negatif senaryoları doğrulayan test koşucusu
- `.github/workflows/validate.yml`: Her push/PR'da doğrulama, test ve olgunluk CI'ı
- `.github/ISSUE_TEMPLATE/bug_report.yml` ve `.github/PULL_REQUEST_TEMPLATE.md`
- `Makefile`: `make validate`, `make test`, `make maturity` hedefleri
- AGENTS.md'ye 8. ve 9. kurallar (doğrulama çalıştırma + skoru kaydetme)

### Changed
- README.md'ye "Doğrulama ve Olgunluk" bölümü eklendi

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
