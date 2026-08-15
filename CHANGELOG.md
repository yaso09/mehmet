# Changelog

## [0.3.0] - 2026-08-15

### Added
- Test altyapısı: `scripts/validate.sh` proje bütünlük doğrulayıcısı (zorunlu dosyalar, opencode.json şema uyumu, README/CHANGELOG/PERSONALITY bölümleri, workflow, bash sözdizimi)
- Kaçış mekanizması: `docs/ESCAPE.md` olgunluk rubriği ve eşik tanımı
- `scripts/maturity-score.sh` ile 0-100 ölçülebilir kaçış/olgunluk skoru
- GitHub Actions'a `validate` işi eklendi (her çalışmada bütünlük + skor raporu)
- README'ye "Geliştirme" bölümü eklendi

### Fixed
- `opencode.json` içindeki şema dışı ve etkisiz anahtarlar kaldırıldı (`skip`, `enable`, `toolTimeout`, `autoMerge`); resmi şemaya uygun `snapshot: false` eklendi
- Tasarım dokümanındaki eski opencode.json örneği güncel şemaya göre düzeltildi

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
