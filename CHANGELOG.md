# Changelog

## [0.3.0] - 2026-08-16

### Added
- `docs/maturity.md`: Ölçülebilir olgunluk kriterleri (escape rubric) — 5 boyut, 0-100 puan
- `docs/progress.md`: İterasyon bazlı olgunluk skoru takibi
- `scripts/validate.sh`: Repo bütünlük doğrulayıcı (dosya varlığı, JSON geçerliliği, secret taraması, trailing whitespace)
- `scripts/score.sh`: Otomatik olgunluk skoru hesaplayıcı (0-100, kaçış eşiği >= 80)
- Workflow'a `validate` job'ı eklendi (her tetikte bütünlük + skor kontrolü)
- `autonomous` ve `comment` job'larına `timeout-minutes: 30` eklendi

### Changed
- AGENTS.md: Kaçış mekanizması ölçülebilir hale getirildi (rubric + score/progress), 8. kural eklendi
- README.md: Proje yapısı ve kaçış mekanizması bölümleri eklendi
- Design doc: Yeni bileşenler (7-10) ve güncellenmiş veri akışı
- Implementation plan'deki trailing whitespace'ler temizlendi

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
