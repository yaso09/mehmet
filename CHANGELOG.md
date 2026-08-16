# Changelog

## [0.3.0] - 2026-08-16

### Added
- MATURITY.md: ölçülebilir kaçış rubriği ve skor kartı (90/100, eşik 90)
- VERSION dosyası ile sürüm yönetimi başlatıldı
- scripts/validate.sh: proje sağlık kontrolü (test altyapısı)
- .github/workflows/ci.yml: her push/PR'da doğrulamayı çalıştıran CI
- opencode.yml otonom job'una "Validate project health" adımı eklendi
- comment job'ına `mentions: "/opencode,/oc"` tetik filtresi eklendi

### Changed
- opencode.json temizlendi: schema'da olmayan `skip`, `enable`, `toolTimeout`, `autoMerge` alanları kaldırıldı, `autoupdate: false` eklendi
- MATURITY.md skoru 85'ten 90'a güncellendi (konfigürasyon temizliği + trigger filtresi)

### Fixed
- opencode.json schema-uyumluluğu sağlandı (K1 kriteri)

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
