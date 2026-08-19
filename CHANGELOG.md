# Changelog

## [0.3.0] - 2026-08-19

### Added
- Repo sağlık kontrolü: scripts/check.py (zorunlu dosyalar, opencode.json şeması, sürüm uyumu, secret sızıntısı tespiti)
- Unit testler: scripts/test_check.py (stdlib unittest)
- Versiyon otomasyonu: VERSION dosyası + scripts/bump_version.py (major/minor/patch)
- CI doğrulama workflow'u: .github/workflows/checks.yml (config, check.py, testler)
- AGENTS.md'ye somut kaçış kontrol listesi (escape path) ve olgunluk puanı eklendi
- README.md'ye geliştirme araçları bölümü eklendi
- .gitignore'a __pycache__/ ve *.pyc eklendi

### Fixed
- opencode.json'daki geçersiz top-level anahtarlar (skip, enable, toolTimeout, autoMerge) kaldırıldı; şemaya uygun geçerli ayarlarla değiştirildi

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
