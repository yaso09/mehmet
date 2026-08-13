# Changelog

## [0.3.0] - 2026-08-13

### Added
- Test altyapısı kuruldu: `scripts/checks.py` (tutarlılık kontrolleri) ve `tests/test_checks.py` (14 birim test)
- `scripts/validate.py` CLI doğrulayıcı (9 kontrol, hata durumunda exit code 1)
- `scripts/maturity.py` olgunluk skoru hesaplayıcı ve `MATURITY.md` üretici (kaçış eşiği: 85+)
- `.github/workflows/ci.yml`: push/PR'da test ve doğrulama çalıştıran CI workflow
- `Makefile`: `test`, `validate`, `maturity`, `check`, `all` hedefleri
- `requirements-dev.txt` (pyyaml bağımlılığı)
- `MATURITY.md`: olgunluk skoru raporu (75/100)

### Fixed
- `opencode.json` geçersiz anahtarlar temizlendi (`skip`, `enable`, `toolTimeout`, `autoMerge` schema'da yok; `additionalProperties: false` nedeniyle opencode başlatmayı bozuyordu). Şema-geçerli `autoupdate`, `share`, `snapshot`, `tool_output`, `compaction` alanlarıyla değiştirildi
- `.gitignore` Python artefaktları için genişletildi (`__pycache__/`, `*.pyc`, `.venv/`)

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
