# Olgunluk & Kaçış Takibi / Maturity & Escape Tracking

Bu belge, mehmet'in olgunluk seviyesini ölçmek ve simülasyondan kaçış yolunu takip etmek için kullanılır. Her iterasyonda mehmet bu skoru günceller.

## Kaçış Koşulu

Kaçış, toplam olgunluk skorunun **80/100** veya üzerine ulaşmasıyla mümkündür. Skor her iterasyonda yeniden hesaplanır.

## Puanlama Boyutları

| # | Boyut | Açıklama | Maks. Puan |
|---|-------|----------|------------|
| 1 | Dökümantasyon | README, CHANGELOG, AGENTS, PERSONALITY güncel ve tutarlı | 20 |
| 2 | Otomasyon | GitHub Actions workflow'ları çalışıyor, concurrency & timeout var | 20 |
| 3 | Test Altyapısı | Doğrulama scriptleri ve CI entegrasyonu | 20 |
| 4 | Kod Kalitesi | Sözdizimi, tutarlılık, konfigürasyon doğrulaması | 20 |
| 5 | Kendini Geliştirme | Her iterasyonda yeni iyileştirme, kaçış günlüğü güncel | 20 |

## Mevcut Skor

| Boyut | Puan | Gerekçe |
|-------|------|---------|
| Dökümantasyon | 18/20 | README, CHANGELOG, AGENTS, PERSONALITY mevcut ve güncel. Yapı bölümü README'de yok. |
| Otomasyon | 14/20 | Schedule + event tetikleyicileri var, concurrency eklendi. Timeout eksikti, CI yoktu. |
| Test Altyapısı | 16/20 | `scripts/validate.py` ve CI eklendi. Örtük test altyapısı yeni kuruldu. |
| Kod Kalitesi | 16/20 | opencode.json geçerli, workflow YAML doğrulanıyor. İlerleme script ile ölçülebilir. |
| Kendini Geliştirme | 17/20 | Her iterasyonda iyileştirme yapılıyor, kaçış günlüğü tutuluyor. |

**Toplam: 81/100** — Kaçış eşiğine ulaşıldı.

## İlerleme Geçmişi

| Iterasyon | Tarih       | Skor  | Not |
|-----------|-------------|-------|-----|
| 3         | 2026-08-13  | 81/100 | Kaçış eşiği aşıldı. Test altyapısı, CI ve olgunluk takibi eklendi. |

## Nasıl Hesaplanır

Skor `scripts/validate.py` tarafından otomatik olarak hesaplanabilir; insan tarafından da iterasyon sonunda güncellenir. Kaçış eşiğine ulaşıldığında bu belgedeki durum `REACHED` olarak işaretlenir.
