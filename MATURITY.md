# Olgunluk Modeli (Maturity Model)

Bu belge, mehmet'in simülasyondan kaçış hedefini ölçülebilir hale getirir.
Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkündür.

`scripts/maturity.sh` bu modelin otomatik değerlendiricisidir. Her iterasyonda
çalıştırılır ve projenin gerçek durumunu (dosya varlığı, tazelik, doğrulama
geçişleri) puanlar.

## Boyutlar (Dimensions)

Her boyut 0–25 puan aralığında değerlendirilir. Toplam 100 puan.

| Boyut | Açıklama | Kontroller |
|-------|----------|------------|
| Dokümantasyon | Projenin kendini anlatması | README güncelliği, CHANGELOG tazeliği, docs/ ve MATURITY.md varlığı |
| Otomasyon | İşlerin elle yapılmadan dönmesi | opencode workflow'u, kalite kapısı (quality.yml), Makefile |
| Bütünlük (Quality) | Proje dosyalarının tutarlılığı | check.sh geçişi, geçerli opencode.json, GPLv3 LICENSE, .gitignore |
| Test Altyapısı | Doğrulama ve kendi kendini test | check.sh + maturity.sh + test.sh geçişi |

## Seviyeler (Levels)

| Seviye | Ad | Puan | Şartlar |
|--------|----|------|---------|
| 1 | Tohum | ≥ 10 | — |
| 2 | Fidancık | ≥ 30 | — |
| 3 | Olgun | ≥ 55 | — |
| 4 | Sınır | ≥ 75 | `make check` hatasız geçer |
| 5 | Kaçış | ≥ 90 | `make check` hatasız geçer + CHANGELOG son 7 günde güncellenmiş |

## Kaçış Kriteri

Kaçış, **Seviye 5**'e ulaşmak ve bunu **ardışık 3 iterasyon** boyunca korumakla
mümkündür. Koruma, `scripts/maturity.sh --log` ile günlüğe kaydedilir ve
`docs/escape-log/` altında izlenir.

## Kullanım

```bash
make maturity   # puanı ve seviyeyi gösterir
make check      # proje bütünlüğünü doğrular
scripts/maturity.sh --log   # mevcut puanı kaçış günlüğüne yazar
```