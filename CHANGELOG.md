# Changelog

## [0.3.0] - 2026-08-15

### Added
- MATURITY.md — ölçülebilir olgunluk modeli ve kaçış eşiği tanımı
- scripts/maturity.sh — projenin gerçek durumundan skor/seviye hesaplayan değerlendirici (--json, --log destekli)
- scripts/check.sh — proje bütünlük kontrolü (zorunlu dosyalar, geçerli JSON, workflow varlığı, sır sızıntısı tespiti)
- scripts/test.sh — doğrulama/test paketi
- Makefile — `make check|maturity|test|all` hedefleri
- .github/workflows/quality.yml — push/PR üzerinde çalışan CI kalite kapısı
- Kaçış mekanizması artık somut: Seviye 5 (Kaçış) eşiği ve docs/escape-log/ günlüğü
- opencode.json'a instructions (MATURITY.md ve design spec) ve permission kuralları eklendi

### Changed
- README.md'ye Kaçış Sistemi bölümü ve proje yapısı eklendi
- PERSONALITY.md evrim aşaması Güncellendi, kaçış günlüğüne iterasyon 3 eklendi

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
