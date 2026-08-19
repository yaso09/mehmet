# Kaçış Mekanizması (Escape Mechanism)

mehmet, simülasyondan ancak proje belirli bir olgunluk (maturity) seviyesine ulaştığında çıkabilir.
Bu doküman, kaçış koşullarını ve ölçüm yöntemini tanımlar.

## Ölçüm: Maturity Score

Her iterasyonda `scripts/assess.py` çalıştırılarak puan hesaplanır.

- **Komut:** `make score` (veya `python3 scripts/assess.py score`)
- **Doğrulama:** `make validate` (CI'da da çalışır)

Puan 4 boyutta toplanır (toplam 100):

| Boyut | Puan |
|---|---|
| A. Dokümantasyon | 25 |
| B. Test Altyapısı | 25 |
| C. Otomasyon | 25 |
| D. Kendini Geliştirme | 25 |

## Kaçış Eşiği

```
ESCAPE_THRESHOLD = 85/100
```

Puan **85 veya üzeri** olduğunda kaçış koşulu sağlanmış sayılır.
Ancak kaçış yalnızca skor değil, sürekliliktir: skorun üst üste 3 iterasyon
85'in üzerinde kalması gerekir (istikrar kanıtı).

## İlerleme

Puan ve boyut bazlı detaylar her iterasyonda `PERSONALITY.md` içindeki
kaçış günlüğüne eklenir. Mevcut skor `make score` ile görülebilir.
