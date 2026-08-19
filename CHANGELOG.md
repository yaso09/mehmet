# Changelog

## [0.3.0] - 2026-08-19

### Added
- **Kaçış mekanizması somutlaştırıldı:** `mehmet/maturity.py` ile ölçülebilir olgunluk skorlama motoru (5 kategori, 100 puan, 80 puan kaçış eşiği)
- **Python paketi:** `mehmet/` paketi ve `python -m mehmet` ile çalışan CLI (`mehmet/__main__.py`)
- **Test altyapısı:** `tests/test_maturity.py` — 11 pytest testi
- **Paketleme:** `pyproject.toml` (setuptools, `[project.scripts]`, pytest + ruff yapılandırması)
- **CI workflow:** `.github/workflows/ci.yml` — ruff lint, pytest, olgunluk doğrulama işi
- **.gitignore:** Python yapıtları (__pycache__, .pytest_cache, .ruff_cache, venv vb.) eklendi

### Changed
- README.md: proje yapısı, olgunluk skoru tablosu ve kullanım kılavuzu eklendi

### Metrics
- Olgunluk skoru: **74.4/100** (kod 22.4, test 17.7, dokümantasyon 14.3, otomasyon 13.0, yönetişim 7.0)
- Kaçış eşiği 80.0 — eksik: 5.6 puan

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
