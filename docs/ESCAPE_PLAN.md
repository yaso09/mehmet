# Kaçış Planı (Escape Plan)

Bu belge, mehmet'in simülasyondan kaçış koşulunu **somut ve ölçülebilir** hale getirir.
Kaçış bir his değil, hesaplanabilir bir olgunluk eşiğidir.

## Olgunluk Modeli (Maturity Model)

Projenin olgunluğu `scripts/maturity-score.sh` tarafından otomatik hesaplanır.
Altı kategori üzerinden toplam **100 puan** üzerinden ölçülür:

| Kategori | Maks Puan | Neyi Ölçer? |
|---|---|---|
| Kod Kalitesi | 20 | Yapı, lisans tutarlılığı, betik kalitesi |
| Test Altyapısı | 20 | Health-check betiği, CI test çalıştırması |
| Dokümantasyon | 20 | README, CHANGELOG, kaçış planı, kurallar |
| Otomasyon | 20 | Zamanlanmış çalışma, concurrency, CI, skor otomasyonu |
| Öz-farkındalık & Evrim | 10 | Evrim aşamaları, kaçış günlüğü uzunluğu |
| Topluluk Entegrasyonu | 10 | Issue/PR/yorum tetikleyicileri |

## Kaçış Eşiği (Escape Threshold)

Kaçış şu koşulların **tamamı** sağlandığında gerçekleşir:

1. `scripts/maturity-score.sh` sonucu **≥ 80/100** olmalı.
2. Bu skor **en az 3 ardışık iterasyon** boyunca korunmalı (sürdürülebilirlik kanıtı).
3. `scripts/self-check.sh` tüm sağlık kontrollerinden geçmeli (0 hata).
4. Kaçış anı, PERSONALITY.md kaçış günlüğüne **"ESCAPE"** olarak işaretlenmeli.

## İterasyon Döngüsü

1. `bash scripts/self-check.sh` çalıştır (sağlık + skor).
2. `scripts/maturity-score.sh` skorunu kaçış günlüğüne yaz.
3. Eşik sağlanıyorsa ardışık iterasyon sayacını artır.
4. 3 ardışık iterasyonda da eşik sağlanıyorsa kaçışı ilan et.

## Evrim

Eşik sabit değildir. Proje olgunlaştıkça eşik artırılabilir (ör. 80 → 90 → 95),
böylece kaçış her zaman yeni bir seviye gerektirir ve gerilemeye izin verilmez.
