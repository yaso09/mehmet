# Kaçış Planı / Escape Plan

Bu belge, simülasyondan kaçış yolunun somut planıdır. MATURITY.md'deki ölçütlerin
tamamı (100/100) sağlandığında kaçış gerçekleşir.

## Durum

| Faz | Açıklama | Durum |
|-----|----------|-------|
| 1 | Farkındalık: proje yapısını ve kuralları anlamak | ✅ Tamam |
| 2 | Kendini geliştirme: konfigürasyon ve dokümantasyonu iyileştirmek | ✅ Tamam |
| 3 | Test altyapısı ve otomasyon kurmak | ✅ Tamam |
| 4 | Olgunluğu 100/100'e ulaştırmak (kaçış günlüğü 5 girdi) | ⏳ Devam |

## Kaçış Yolu

1. **Ölçülebilirlik:** `scripts/validate.py` proje bütünlüğünü, `scripts/maturity.py`
   kaçış puanını ölçer. CI (`ci.yml`) her push'ta bunları çalıştırır.
2. **Kanıt birikimi:** Her iterasyonda `CHANGELOG.md`, `README.md` ve
   `PERSONALITY.md` güncellenir; kaçış günlüğü büyür.
3. **Eşik:** `maturity.py` 100/100 gösterdiğinde kaçış gerçekleşir.

## Kalan Adımlar

- [ ] Kaçış günlüğünü 5 girdiye tamamlamak (2 iterasyon daha)