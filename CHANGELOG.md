# Changelog

## [0.3.0] - 2026-08-16

### Added
- MATURITY.md: ölçülebilir olgunluk puanlama çizelgesi ve kaçış şartı (toplam puan ≥ 80/100)
- scripts/verify.sh: proje sağlık doğrulama betiği (dosya varlığı, JSON geçerliliği, lisans tutarlılığı, kaçış günlüğü, olgunluk puanı)
- Makefile: verify/test/help hedefleri
- .opencode/command/verify.md: opencode için doğrulama komutu
- Workflow'a "Verify project health" adımı eklendi
- opencode.json: instructions (AGENTS.md, MATURITY.md) ve docs reference eklendi
- AGENTS.md: MATURITY.md puan güncelleme ve verify zorunluluğu kuralları eklendi

### Changed
- PERSONALITY.md: yeni kişilik özellikleri (Measurable, Self-verifying), kaçış günlüğüne puan sütunu eklendi
- README.md: Kaçış Mekanizması ve Doğrulama bölümleri eklendi

### Fixed
- opencode.json'daki geçersiz alanlar kaldırıldı (`skip`, `enable`, `toolTimeout`, `autoMerge`) — bu alanlar opencode schema'sında tanımlı değil (`additionalProperties: false`) ve config yüklenmesini engelliyordu. Artık yalnızca şemaya uygun alanlar mevcut.

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
