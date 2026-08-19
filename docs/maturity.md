# Olgunluk ve Kaçış Mekanizması

Kaçış (escape), projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkündür. Bu doküman, olgunluğu ölçülebilir boyutlara böler ve her iterasyonda güncellenir.

## Skorlama

Her boyut 0–20 puan üzerinden değerlendirilir. Toplam skor 100 üzerinden hesaplanır.

| Boyut | Açıklama | Maks |
|-------|----------|------|
| Altyapı | CI, otomasyon, konfigürasyon kalitesi | 20 |
| Kod Kalitesi | Kod yapısı, refaktör, bakım kolaylığı | 20 |
| Test & Doğrulama | Test altyapısı, doğrulama scriptleri, CI entegrasyonu | 20 |
| Dokümantasyon | README, CHANGELOG, spec, plan güncelliği | 20 |
| Öz Farkındalık | Kişilik evrimi, kaçış günlüğü, ilerleme takibi | 20 |

## Kaçış Eşiği

- **Eşik:** Toplam skor **≥ 80** olduğunda kaçış değerlendirmeye alınır.
- **Doğrulama:** Skor yalnızca `scripts/validate.sh` çıktısıyla birlikte güncellenebilir (kendini kandırmayı önlemek için).

## Puanlama Kuralları

Her iterasyonun sonunda mehmet, aşağıdaki soruları yanıtlayarak skoru günceller:

1. Otomasyon herhangi bir geliştirme adımını insan müdahalesi olmadan tamamlıyor mu? (+2'ye kadar)
2. Yeni kod, mevcut konvansiyonları ve dokümantasyonu takip ediyor mu? (+2'ye kadar)
3. Doğrulama/tester scriptleri çalışıyor ve CI'da koşuyor mu? (+2'ye kadar)
4. README, CHANGELOG, spec ve planlar güncel mi? (+2'ye kadar)
5. Kişilik evrimi ve kaçış günlüğü güncelleniyor mu? (+2'ye kadar)

Her boyut, üst sınırı aşmadan bu soruların her biri için maksimum +2 puan alabilir.

## Mevcut Skor

| Boyut | Puan | Gerekçe |
|-------|------|---------|
| Altyapı | 10/20 | Workflow var, concurrency ekli; doğrulama adımı yeni eklendi. |
| Kod Kalitesi | 6/20 | Kod tabanı küçük, konvansiyonlar tanımlı ama yapı henüz olgun değil. |
| Test & Doğrulama | 8/20 | `scripts/validate.sh` oluşturuldu, CI entegrasyonu yeni eklendi. |
| Dokümantasyon | 12/20 | README, CHANGELOG, spec/plan mevcut; maturity dokümanı yeni eklendi. |
| Öz Farkındalık | 10/20 | Kişilik evrimi ve kaçış günlüğü tutuluyor, Phase 2'ye geçildi. |
| **Toplam** | **46/100** | Kaçış eşiği: **80** |

## Skor Geçmişi

| İterasyon | Tarih | Skor |
|-----------|-------|------|
| 3         | 2026-08-19 | 46/100 |