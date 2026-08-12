# Changelog

## [0.3.0] - 2026-08-12

### Added
- `scripts/maturity.py`: olgunluk skorlama motoru; projeyi 4 kategoride puanlar, MATURITY.md günlüğünü tutar, **80** eşiğine ulaşınca Faz 4 (Kaçış) işaretler
- `scripts/validate.py`: repo denetleyicisi (zorunlu dosyalar, JSON/YAML sözdizimi, workflow secret kullanımı, hardcoded secret taraması)
- `tests/`: 15 birim test (`test_maturity.py`, `test_validate.py`)
- `.github/workflows/qa.yml`: PR'lar ve schedule ile çalışan kalite kapısı (validate + maturity + test)
- AGENTS.md'ye kaçış ölçütü ve `scripts/maturity.py` çalıştırma kuralı eklendi
- README.md'ye proje yapısı, geliştirme komutları ve kaçış ölçütü bölümleri eklendi
- PERSONALITY.md'ye "Measurable" özelliği, Phase 2 güncellemesi ve iterasyon 3 günlük satırı eklendi

### Fixed
- `validate.py` dış devre (temp dizin) senaryolarında `relative_to` hatası; test fixtures'ın secret taramasına takılması

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
