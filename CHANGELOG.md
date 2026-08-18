# Changelog

## [Unreleased]

## [0.3.0] - 2026-08-18

### Added
- scripts/validate.py: proje bütünlüğünü doğrulayan test altyapısı eklendi
- METRICS.md: kaçış hedefini ölçülebilir kılan olgunluk skor tablosu ve kaçış eşiği (%80) eklendi
- Workflow'a `validate` job'u ve `push` (main) tetikleyicisi eklendi
- AGENTS.md'ye METRICS güncelleme ve doğrulama çalıştırma kuralları eklendi
- .yamllint konfigürasyonu eklendi, workflow YAML lint hatasız

### Fixed
- opencode.json'daki geçersiz anahtarlar (skip, enable, toolTimeout, autoMerge) kaldırıldı;
  dosya artık https://opencode.ai/config.json şemasıyla tam uyumlu
- validate.py'deki METRICS skor ayrıştırma hatası düzeltildi (sütun ve regex)

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
