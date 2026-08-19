# Changelog

## [0.3.0] - 2026-08-19

### Added
- `scripts/health_check.py`: Olgunluk (maturity) skorlayıcı ve proje sağlık kontrolü (0-100 skor, 90 kaçış eşiği)
- `docs/maturity.md`: Kaçış eşiği ve skor kartı dokümanı
- `.github/workflows/validate.yml`: Her push/PR'da çalışan otomasyonlu sağlık kontrolü
- README'ye "Gelişim ve Olgunluk" bölümü eklendi

### Fixed
- `health_check.py` schedule+dispatch kontrolündeki dosya-adı yanlış okuma hatası düzeltildi
- `health_check.py` yapı kategorisi puan dağılımı düzeltildi (30 puana sabitlendi, toplam 100/100 sınırı)

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
