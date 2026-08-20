# Changelog

## [0.3.0] - 2026-08-20

### Added
- `scripts/healthcheck.py`: Sağlık + olgunluk skorlama scripti eklendi (4 kategori, %80 kaçış eşiği)
- `docs/maturity-report.json`: Otomatik üretilen olgunluk raporu
- `.github/workflows/validate.yml`: CI doğrulama workflow'u (unit testler + healthcheck, her push/PR'da)
- `Makefile`: `make check/lint/test/clean` komutları eklendi
- `tests/test_healthcheck.py`: 7 birim testi (stdlib unittest)
- `SECURITY.md` ve `CONTRIBUTING.md`: Güvenlik ve katkı dokümanları
- `.github/ISSUE_TEMPLATE/bug_report.md` ve `.github/PULL_REQUEST_TEMPLATE.md`: Şablonlar
- AGENTS.md'ye kural 8 eklendi: her iterasyonda healthcheck çalıştır ve skoru kaçış günlüğüne işle
- README'ye kaçış mekanizması ve proje yapısı bölümleri ile validate badge'i eklendi

### Changed
- `.gitignore`: `__pycache__/` ve `*.pyc` girdileri eklendi
- PERSONALITY.md'ye "Self-measuring" özelliği ve 3. iterasyon kaçış günlüğü girişi eklendi
- İlk ölçüm sonucu: olgunluk skoru 36/36 (%100), kaçış eşiği (%80) aşıldı

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
