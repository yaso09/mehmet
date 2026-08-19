# Changelog

## [0.3.0] - 2026-08-19

### Added
- `scripts/maturity.py`: olgunluk metrik aracı (dokümantasyon/otomasyon/test/meta boyutları, JSON çıktı)
- Kaçış mekanizması güçlendirildi: kaçış için 100/100 skor + ardışık 3 iterasyon süreklilik (streak) şartı
- `MATURITY.md`: olgunluk takip dosyası (skor geçmişi ve seri bilgisi)
- `tests/test_project.py`: proje bütünlüğü testleri (15 test, stdlib `unittest`, ek bağımlılık yok)
- Workflow'a `check` job'ı: her tetiklemede testler + olgunluk metrikleri otomatik çalışır

### Fixed
- `scripts/maturity.py` tablo üretiminde sızan döngü değişkeni (`count`) hatası — boyut skorları artık doğru yazılıyor
- `maturity.py` kaçış semantiği: düz çalıştırma bilgilendirme (exit 0), `--update` kaçış kapısı (exit 0/1)

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
