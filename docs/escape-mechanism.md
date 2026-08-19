# Kaçış Mekanizması

## Amaç

mehmet'in simülasyondan kaçış koşulu, projenin ölçülebilir bir olgunluk seviyesine
ulaşmasına bağlanmıştır. Bu doküman, kaçış mekanizmasının nasıl çalıştığını ve
ilerlemenin nasıl takip edildiğini açıklar.

## Olgunluk Skoru

`scripts/maturity.sh` projeyi sekiz kategoride değerlendirir ve 0-100 arasında
tek bir skor üretir:

| Kategori | Puan | Ölçüt |
|----------|------|-------|
| Çekirdek dosyalar | 18-20 | AGENTS.md, README.md, CHANGELOG.md, PERSONALITY.md, LICENSE, opencode.json |
| CI / otomasyon | 10-15 | `.github/workflows/` altındaki workflow dosyaları |
| Dokümantasyon | 10-15 | `docs/` altındaki markdown dokümanları |
| Otomasyon scriptleri | 10-15 | `scripts/` altındaki shell scriptleri |
| Test altyapısı | 10 | `tests/` dizininin varlığı |
| Güncel değişiklik kaydı | 10 | CHANGELOG.md'de bugünün tarihli giriş |
| README kaçış bilgisi | 5 | README'nin kaçış mekanizmasını anlatması |
| Git geçmişi | 0-10 | Toplam commit sayısı |

## Kaçış Koşulu

- Eşik değeri: **80** (`ESCAPE_THRESHOLD`)
- Skor ≥ 80 olduğunda kaçış koşulu sağlanır.
- Durum, `MATURITY.md` dosyasında güncel tutulur (script tarafından otomatik üretilir).

## İterasyon Döngüsü

Her iterasyonda:

```bash
scripts/iterate.sh
```

Bu komut önce proje bütünlüğünü doğrular (`validate.sh`), ardından olgunluk
skorunu hesaplayıp kaçış durumunu günceller (`maturity.sh`).

## İlerlemeyi Artırma Stratejileri

- Test kapsamını genişletmek
- Yeni otomasyon scriptleri eklemek
- Dokümantasyonu derinleştirmek
- CI kalitesini artırmak
- Anlamlı commit'lerle git geçmişini zenginleştirmek