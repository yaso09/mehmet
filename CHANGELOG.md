# Changelog

## [0.4.0] - 2026-08-19

### Added
- Kaçış koşulu SAĞLANDI: olgunluk skoru 83/100 ile 80 eşiğini aştı
- `docs/escape-mechanism.md`: kaçış mekanizmasının detaylı dokümantasyonu
- `docs/testing.md`: test altyapısı dokümantasyonu
- `scripts/summarize.sh`: iterasyon başında proje durum özeti aracı
- MATURITY.md artık kaçış durumunu otomatik takip ediyor

## [0.3.0] - 2026-08-19

### Added
- Kaçış mekanizması uygulandı: `scripts/maturity.sh` olgunluk skorunu (0-100) hesaplar ve `MATURITY.md` üretir
- `scripts/validate.sh` ile proje bütünlüğü doğrulaması (JSON, YAML, shellcheck, dosya varlığı)
- `scripts/iterate.sh` standart iterasyon döngüsü (doğrulama + olgunluk)
- Test altyapısı: `tests/run.sh` çalıştırıcısı, maturity ve validate testleri
- `.github/workflows/validate.yml` CI doğrulama workflow'u (push/PR)
- AGENTS.md'ye kaçış mekanizması bölümü eklendi
- README.md'ye scriptler, testler ve CI bölümleri eklendi

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
