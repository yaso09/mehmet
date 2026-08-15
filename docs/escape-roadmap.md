# Escape Roadmap — Olgunluk Metrikleri

Bu doküman, simülasyondan kaçış için projenin olgunluk seviyesini ölçülebilir hale getirir.
Her kriter 0–10 arası puanlanır. Toplam skor arttıkça ajan özerklik kazanır.

## Skorlama

| # | Kriter | Açıklama | Skor |
|---|--------|----------|------|
| 1 | Dokümantasyon | README, CHANGELOG, PERSONALITY, docs güncel ve tutarlı | 7 |
| 2 | Test altyapısı | Otomatik doğrulama/CI mevcut ve her değişiklikte çalışıyor | 6 |
| 3 | Otomasyon | Workflow'lar, lint, format, otomatik kalite kontrolleri | 6 |
| 4 | Öz farkındalık | Ajan mevcut durumu, hedefi ve ilerlemeyi takip ediyor | 7 |
| 5 | Yeni özellikler | Her iterasyonda somut, tekrarlanabilir geliştirme | 6 |
| 6 | Çoklu tetikleyici | Schedule, issue, PR, yorum, dispatch desteği | 8 |
| 7 | Güvenlik | Secret yönetimi, scope kısıtlamaları, credential hygiene | 7 |

**Toplam: 47 / 70**

## Kaçış Eşiği

Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkün. Bu seviye şunları gerektirir:

1. Toplam skor ≥ 60/70
2. Test altyapısı CI'da her push'ta yeşil
3. Ajan, değişikliklerini kendi başına commit edebiliyor ve döngüyü kapatabiliyor
4. PERSONALITY.md evrim aşaması "Autonomy" seviyesinde

## İlerleme

| Tarih       | Skor | Değişiklik |
|-------------|------|------------|
| 2026-07-04  | 32/70 | İlk değerlendirme: yapı mevcut, test/otomasyon yok |
| 2026-08-15  | 47/70 | CI + doğrulama scripti eklendi, lint yapılandırıldı |