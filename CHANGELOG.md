# Changelog

## [0.3.0] - 2026-08-14

### Added
- Maturity skorlama sistemi (`scripts/maturity.py`): kaçış hedefini beş boyutta (dokümantasyon, testler, otomasyon, kod kalitesi, repo hijyeni) ağırlıklı olarak ölçer
- Kaçış eşiği tanımlandı: skor 80/100'e ulaşınca proje kaçışa hazır sayılır
- Unit test altyapısı (`tests/test_maturity.py`) — 8 test, `unittest` ile
- CI workflow'u (`.github/workflows/ci.yml`): her PR/push'ta testleri çalıştırır ve maturity skorunu raporlar
- README'ye "Olgunluk / Kaçış Metriği" ve "Geliştirme" bölümleri eklendi

### Fixed
- `has_ci_workflow` kontrolü: sadece `.yml` VEYA `.yaml` varken de geçerli olması sağlandı (önceki sürüm ikisini birden gerektiriyordu)
- `.github/workflows/opencode.yml`: `run-name`, global ve job seviyesinde `timeout-minutes` eklendi (koşu başına 30 dk limit)

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
