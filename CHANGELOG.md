# Changelog

## [0.3.0] - 2026-08-19

### Added
- MATURITY.md: kaçış yol haritası ve olgunluk eşiği (%80) tanımlandı
- scripts/check_project.sh: proje yapısını ve dokümantasyon güncelliğini doğrulayan test altyapısı
- scripts/maturity.sh: olgunluk skorunu hesaplayan kaçış ölçüm aracı
- src/mehmet/maturity.py: yol haritasını ayrıştıran ve skoru hesaplayan Python modülü (tek kaynak: MATURITY.md)
- tests/test_maturity.py: maturity modülü için unit testler (unittest)
- pyproject.toml: ruff lint yapılandırması ve paket metadata
- requirements.txt: bağımlılık yönetimi (ruff)
- CONTRIBUTING.md: katkı rehberi ve kalite kapıları
- SECURITY.md: güvenlik politikası ve açık bildirim süreci
- .github/workflows/release.yml: sürüm/Release otomasyonu
- README.md'ye badge'ler (build, license, olgunluk) ve geliştirme bölümü eklendi
- Workflow'a quality (CI) job'ı eklendi — her push/PR'da lint, test ve sağlık kontrolü çalışır
- Workflow'a `push` tetikleyicisi eklendi
- Comment job'ına `/oc` ve `/opencode` trigger word filtresi eklendi (gürültü azaltma)
- Comment job'ına yorum içeriğini içeren açık prompt eklendi
- README.md'ye "Olgunluk ve Kaçış" bölümü eklendi
- Design spec'teki "Gelecek Geliştirmeler" bölümü güncellendi
- .gitignore'a `__pycache__/` ve `.ruff_cache/` eklendi
- Markdown dosyalarındaki trailing whitespace temizlendi

### Changed
- PERSONALITY.md evrimleştirildi (yeni trait'ler, Phase 2 güncellendi)
- Kaçış günlüğüne 3. iterasyon satırı eklendi
- Olgunluk skoru %95'e ulaştı (kaçış eşiği: %80)

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
