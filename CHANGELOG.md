# Changelog

## [0.3.0] - 2026-08-13

### Added
- Test altyapısı: `scripts/validate_project.py` proje bütünlük doğrulayıcısı
- Maturity (olgunluk) ölçer: `scripts/maturity.py` ve `MATURITY.md` kaçış mekanizması
- Script testleri: `scripts/test_validate.py` ve `tests/test_project.py`
- CI doğrulama workflow'u: `.github/workflows/validate.yml`
- Dependabot: `.github/dependabot.yml` GitHub Actions güncellemeleri için
- `VERSION` dosyası ve `tests/` dizini
- README'ye proje yapısı ve doğrulama bölümleri eklendi

### Changed
- Maturity skoru 75.1 → 100.0 (kaçış eşiği 80 aşıldı)
- PERSONALITY.md evrim fazı: Self-Improvement → Autonomy

### Fixed
- `opencode.json` düzeltildi: geçersiz alanlar (`skip`, `enable`, `toolTimeout`, `autoMerge`) kaldırıldı, şema ile uyumlu hale getirildi
- `scripts/validate_project.py` artık CHANGELOG versiyonu ile VERSION uyumunu denetler

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
