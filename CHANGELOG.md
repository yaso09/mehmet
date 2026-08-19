# Changelog

## [0.3.0] - 2026-08-19

### Added
- Test altyapısı: `tests/test_project.py` (17 unittest senaryosu)
  - Proje bütünlüğü: gerekli dosyalar, boş olmama kontrolü
  - opencode.json JSON geçerliliği ve model doğrulaması
  - Workflow'un schedule/autonomous/comment içermesi
  - CHANGELOG semver ve güncellik kontrolü
  - README gerekli bölümleri ve lisans uyumu
  - PERSONALITY.md kaçış günlüğü ve evrim aşamaları
  - AGENTS.md simülasyon bağlamı ve kaçış hedefi
  - Gizli API anahtarı (secret) sızıntısı taraması
  - LICENSE GPLv3 uyumluluğu
- CI workflow: `.github/workflows/ci.yml` (test + lint)
- Makefile: `test`, `lint`, `check`, `json`, `clean` hedefleri

### Changed
- README.md'ye Mimari ve Geliştirme bölümleri eklendi
- .gitignore'a Python cache desenleri eklendi (`__pycache__/`, `*.py[cod]`)

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
