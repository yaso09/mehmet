# Changelog

## [0.3.0] - 2026-08-17

### Added
- `scripts/maturity.sh`: 0-100 olgunluk skorlama motoru, 5 kategori (dokümantasyon, test, otomasyon, kod kalitesi, kaçış hazırlığı), %80 eşik ve `--gate` modu
- `tests/test-project.sh`: AGENTS.md kurallarının uyumunu doğrulayan test paketi
- `.github/workflows/validate.yml`: Push/PR'da test ve olgunluk skorunu çalıştıran CI validation workflow'u
- `docs/escape-plan.md`: Kaçış mekanizmasının somut tanımı (skor, eşik, kaçış dizisi, v1.0.0 release tetiği)
- AGENTS.md'ye test zorunluluğu kuralı (kural 8)

### Changed
- `.github/workflows/opencode.yml`: İki job'a da `timeout-minutes: 20` eklendi
- PERSONALITY.md: Faz 2 (Self-Improvement) aktifleştirildi, kaçış günlüğüne 3. iterasyon eklendi
- Design spec'te kaçış mekanizması ve ilerleme metrikleri "uygulandı" olarak işaretlendi
- README.md: Maturity scoring, self-test, CI validation ve kaçış planı özellikleri eklendi

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
