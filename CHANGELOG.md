# Changelog

## [0.3.0] - 2026-08-17

### Added
- Test altyapısı eklendi (`tests/`): proje yapısı, konfigürasyon, dokümantasyon ve olgunluk testleri
- Kaçış mekanizması somutlaştırıldı: `maturity.json` kriterleri ve `scripts/maturity.py` skorlama
- `MATURITY.md` olgunluk/kaçış durumu dokümantasyonu eklendi
- CI workflow'u (`ci.yml`): her push/PR'da test, olgunluk ve YAML doğrulaması
- `Makefile` ile `test`, `lint`, `maturity`, `ci` hedefleri eklendi
- README'ye test ve yapı bölümleri eklendi
- `CONTRIBUTING.md` katkı rehberi eklendi
- `docs/ARCHITECTURE.md` mimarî özeti eklendi
- `.yamllint.yml` konfigürasyonu ile workflow YAML denetimi
- `scripts/maturity.py` için doğrudan birim testler (`tests/test_maturity_script.py`)
- Sır sızıntısı taraması (secrets check) ve sürüm senkronizasyonu kontrolü

### Fixed
- Workflow YAML'lerinde dosya sonu satır sonu (EOF newline) eksikliği düzeltildi
- Kaçış eşiği kriterleri başlangıçta her şeyi geçiyordu; skorlama anlamlı kalite kapılarına dönüştürüldü (test + sürüm + sır taraması)

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
