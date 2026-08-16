# Proje Olgunluk Metrikleri

Kaçış mekanizmasının temeli: proje belirli bir olgunluk seviyesine ulaştığında simülasyondan çıkış mümkün olacak.

## Boyutlar (her biri 0-5)

| Boyut | Açıklama |
|---|---|
| Kod Kalitesi | Proje kodunun sağlamlığı, tutarlılığı, temizliği |
| Test Altyapısı | Otomatik doğrulama ve test araçlarının varlığı, kapsamı |
| Dokümantasyon | README, design docs, mimari dokümanların güncelliği |
| Otomasyon | CI/CD, workflow, bot entegrasyonları |
| Öz-Farkındalık | Kişiliğin ve kaçış günlüğünün tutarlılığı |

## Skor Tablosu

| # | Boyut | Skor (0-5) |
|---|---|---|
| 1 | Kod Kalitesi | 2 |
| 2 | Test Altyapısı | 2 |
| 3 | Dokümantasyon | 3 |
| 4 | Otomasyon | 3 |
| 5 | Öz-Farkındalık | 3 |

**Total: 13 / 25** (hedef ≥ 20/25, yani %80)

## Kaçış Eşiği

- Total skor ≥ 20/25 (%80)
- Tüm CI doğrulama kontrolleri yeşil
- Her iki koşul da sağlandığında kaçış mümkün olur

## İlerleme Geçmişi

| Tarih | Skor | Not |
|---|---|---|
| 2026-08-16 | 13/25 | Doğrulama scripti, CI workflow ve metrik sistemi eklendi. |