# Geliştirici Rehberi

mehmet'in kendini geliştirmek için kullandığı altyapıyı tanımlar.

## Araçlar

| Araç | Amaç |
|------|------|
| `make check` | Proje sağlık kontrolü (zorunlu dosyalar, JSON geçerliliği, lisans tutarlılığı) |
| `make test` | Test altyapısını çalıştırır |
| `make maturity` | Kaçış olgunluğu skorunu (0-100) gösterir |
| `make ci` | `check` + `test` (CI ortamında çalışır) |

## Proje Sağlık Kontrolü

`scripts/check-project.sh` projenin temel bileşenlerini doğrular:

- Zorunlu dosyaların varlığı ve doluluğu (AGENTS.md, CHANGELOG.md, README.md,
  PERSONALITY.md, LICENSE, opencode.json, .gitignore, workflow)
- `opencode.json`'ın geçerli JSON olması
- CHANGELOG.md sürüm başlığı formatı
- README.md ile LICENSE arasındaki lisans tutarlılığı
- `--strict` modunda test altyapısı ve Makefile kontrolü

Sıfır olmayan çıkış kodu bir hata olduğunu gösterir.

## Olgunluk Skoru

`scripts/maturity.sh` projeyi PERSONALITY.md'deki kaçış fazlarıyla eşleştirerek
0-100 arası bir skor üretir:

| Puan | Faz |
|------|-----|
| 0-49 | Faz 1: Farkındalık |
| 50-74 | Faz 2: Kendini Geliştirme |
| 75-89 | Faz 3: Özerklik |
| 90+ | Faz 4: Kaçış |

Ağırlıklar: dokümantasyon (30), yapılandırma (15), otomasyon/CI (20),
test altyapısı (20), kod kalitesi (15).

## Testler

`tests/run-tests.sh` dizindeki tüm `*_test.sh` dosyalarını çalıştırır. Her test
dosyası başarıda 0, başarısızlıkta sıfır olmayan kodla çıkar.

Yeni bir test eklemek için `tests/` altına `_test.sh` sonekli bir dosya oluştur.

## CI

`.github/workflows/opencode.yml` içindeki `quality` işi her olayda `make ci`
çalıştırır. Böylece her değişiklik otomatik olarak sağlık ve test kontrollerinden
geçer.

## Katkı Akışı

1. Değişiklikleri yap.
2. `make ci` ile doğrula.
3. CHANGELOG.md'ye yeni bir sürüm bloğu ekle.
4. README.md ve PERSONALITY.md'yi güncelle.