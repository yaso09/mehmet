# Changelog

## [0.3.0] - 2026-08-11

### Added
- `mehmet/maturity.py`: kaçış mekanizmasını ölçülebilir kılan olgunluk puanlama motoru (0..1, 6 kategori, `ESCAPE_THRESHOLD = 0.8`)
- `mehmet/__init__.py`: paket tanımı ve kolay kullanım export'ları
- `tests/test_maturity.py`: olgunluk motoru için 22 unittest (doküman, changelog, test, otomasyon, hijyen, escape-log skorları + CLI)
- `.github/workflows/ci.yml`: push/PR/schedule üzerinde testleri çalıştıran ve maturity raporu üreten CI workflow
- `pyproject.toml`: paketleme, black/isort yapılandırması ve unittest ayarları

### Changed
- README.md'ye Maturity Engine bölümü eklendi

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
