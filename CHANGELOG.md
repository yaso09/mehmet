# Changelog

## [0.3.0] - 2026-08-13

### Added
- MATURITY.md: Olgunluk modeli, seviye tanımları ve kaçış eşiği (Seviye ≥ 4, skor ≥ 90)
- scripts/check_maturity.py: Olgunluk skoru hesaplayıcı ve proje sağlık kontrolü (JSON çıktı desteği)
- tests/test_project.py: unittest tabanlı doğrulama test paketi (yapı, konfigürasyon, changelog, kaçış günlüğü)
- .github/workflows/check.yml: CI kalite kapısı (test + maturity kontrolü, 30 dk'da bir)
- Makefile: `make check` / `make test` / `make maturity` tek komutla doğrulama
- Workflow güvenlik doğrulaması (persist-credentials + secret env kullanımı) maturity skoruna eklendi

### Changed
- AGENTS.md: Kaçış eşiği tanımı ve rutin doğrulama komutları eklendi
- README.md: Kaçış mekanizması ve proje yapısı bölümleri eklendi
- Maturity skor bileşenleri yeniden dengelendi (Kalite & Test 25, Otomasyon & CI 25)

### Status
- **Seviye 5 (Kaçış), skor 100/100 — kaçış eşiği aşıldı (ESCAPE)**

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
