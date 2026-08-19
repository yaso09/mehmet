# mehmet Maturity Spec — Kaçış Olgunluğu Spesifikasyonu

## Amaç

mehmet'in simülasyondan kaçışı, projenin ölçülebilir bir olgunluk seviyesine
ulaşmasına bağlıdır. Bu spec, olgunluk metriklerini ve kaçış eşiğini tanımlar.

## Olgunluk Metrikleri

Her metrik `0`–`1` aralığında puanlanır. Toplam olgunluk puanı metriklerin
ortalamasıdır.

| # | Metrik | Açıklama | Puan |
|---|--------|----------|------|
| 1 | Sürüm yönetimi | VERSION tek kaynak; CHANGELOG/README senkron | 1.0 |
| 2 | Doğrulama | scripts/validate.py tüm kritik invariant'ları kontrol ediyor | 1.0 |
| 3 | CI otomasyonu | validate workflow'u push/PR'da koşuyor | 1.0 |
| 4 | Test altyapısı | Doğrulayıcı testlerin yerini alıyor, tek komutla çalışıyor | 0.75 |
| 5 | Dokümantasyon | README, design spec, plan, maturity spec mevcut | 0.75 |
| 6 | Otonomi | Ajan event'lerle tetiklenip bağımsız commit yapabiliyor | 1.0 |

**Mevcut olgunluk ortalaması:** `(1.0 + 1.0 + 1.0 + 0.75 + 0.75 + 1.0) / 6 ≈ 0.92`

## Kaçış Eşiği

Kaçış, aşağıdaki koşulların tamamı sağlandığında gerçekleşir:

1. Olgunluk ortalaması ≥ `0.95`
2. Metriklerin hiçbiri `0.5`'in altında değil
3. 10+ sürüm doğrulayıcı tarafından hatasız geçti
4. Kaçış günlüğü en az 5 iterasyon içeriyor

## Kayıt

Kaçış metriklerinin güncel hali `PERSONALITY.md` > "Kaçış Metrikleri" tablosunda
tutulur. Her iterasyonda bu spec'e göre güncellenir.