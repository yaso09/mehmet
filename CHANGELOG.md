# Changelog

## [0.3.0] - 2026-08-16

### Added
- Maturity/kaçış mekanizması: `src/mehmet/maturity.py` ile proje olgunluğu beş boyutta ölçülür, `ESCAPE_THRESHOLD` (75) aşıldığında durum `escaped` olarak raporlanır
- CLI: `python -m mehmet [path]` ile skor raporu, `--json` çıktı desteği
- Test altyapısı: `tests/test_maturity.py` (unittest, 5 test)
- Paketleme: `pyproject.toml` + `mehmet` konsol komutu
- Otomasyon: `Makefile` (test/maturity/validate/install/clean hedefleri)
- CI doğrulama: `.github/workflows/ci.yml` (testler + maturity skoru)
- AGENTS.md'ye kaçış mekanizması ve `make` komutları eklendi
- README.md'ye kaçış mekanizması ve proje yapısı bölümleri eklendi

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
