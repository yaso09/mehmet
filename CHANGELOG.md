# Changelog

## [0.3.0] - 2026-08-14

### Added
- `scripts/maturity.py`: Kaçış eşiğini ölçen olgunluk (maturity) skorlayıcısı eklendi. Yapı, otomasyon, dokümantasyon ve kalite boyutlarında 26 puan üzerinden skor üretir; `--json` ve `--threshold` seçenekleri destekler.
- `tests/test_maturity.py`: Olgunluk skorlayıcısı için 10 adet unittest eklendi (harici bağımlılık yok).
- `.github/workflows/validate.yml`: Test, sözdizimi ve olgunluk kontrolü yapan CI workflow eklendi. Maturity skoru eşiğin altına düşerse build başarısız olur (regresyon koruması).

### Changed
- Kaçış mekanizması artık somut: `scripts/maturity.py` ile ölçülen maturity skoru ve CI'daki `--threshold 22` eşiği ile izleniyor.

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
