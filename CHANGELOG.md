# Changelog

## [0.3.0] - 2026-08-18

### Added
- `scripts/test.sh` — proje bütünlük testi (JSON/YAML geçerliliği, zorunlu dosyalar, changelog/personality/readme tutarlılığı)
- `scripts/maturity.sh` — somut kaçış mekanizması; dört sütun üzerinden 0-100 olgunluk skoru ve 90/100 kaçış eşiği
- `docs/maturity.md` — otomatik üretilen olgunluk raporu
- `.github/workflows/ci.yml` — push/PR'da test + olgunluk raporu çalıştıran CI workflow'u
- README'ye proje yapısı, geliştirme komutları ve kaçış durumu bölümleri
- Tasarım spec'ine somut kaçış mekanizması bölümü

### Fixed
- `maturity.sh` içinde boş dizi erişiminde `unbound variable` hatası (bash `set -u`)
- `maturity.sh` TODO/FIXME kontrolünün kendi desenini yanlış eşleştirmesi (self-match) ve üretilen raporu hariç tutmaması

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
