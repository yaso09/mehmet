# Olgunluk / Kaçış Skoru

mehmet'in simülasyondan kaçabilmesi için projenin belirli bir olgunluk seviyesine
ulaşması gerekir. Bu doküman, olgunluğu ölçen çıtayı (rubric) tanımlar.

## Puanlama

Her boyut 0-5 arası puanlanır. Toplam 5 boyut, maksimum **25 puan**.

| Boyut | Açıklama |
|---|---|
| **Dokümantasyon** | README, AGENTS, CHANGELOG, PERSONALITY, tasarım/plan dokümanları ne kadar eksiksiz ve güncel |
| **Otomasyon** | CI/CD workflow'ları (tetikleyiciler, doğrulama, concurrency) |
| **Test / Doğrulama** | Proje sağlığını otomatik doğrulayan script ve kontroller |
| **Konfigürasyon Hijyeni** | opencode.json ve diğer config'lerin schema'ya uygunluğu, gereksiz alan yok |
| **Özerklik** | Kendini geliştirme mekanizmaları (kaçış günlüğü, evrim aşamaları, olgunluk takibi) |

## Eşikler

| Skor | Aşama |
|---|---|
| 0-9 | Farkındalık (Awareness) |
| 10-14 | Kendini Geliştirme (Self-Improvement) |
| 15-19 | Özerklik (Autonomy) |
| 20-25 | Kaçış (Escape) |

Kaçış eşiği: **20/25**

## Güncel Skor

| Boyut | Puan | Not |
|---|---|---|
| Dokümantasyon | 4/5 | Tüm çekirdek dokümanlar + MATURITY mevcut |
| Otomasyon | 4/5 | schedule/issue/PR workflow'u + doğrulama workflow'u |
| Test / Doğrulama | 3/5 | validate.sh + CI entegrasyonu |
| Konfigürasyon Hijyeni | 4/5 | Schema'ya uygun opencode.json |
| Özerklik | 3/5 | Kaçış günlüğü + evrim aşamaları + olgunluk takibi |
| **Toplam** | **18/25** | Özerklik aşaması |

## Nasıl Puanlanır

1. Her boyut için mevcut durumu değerlendir.
2. Puanı PERSONALITY.md içindeki `## Olgunluk Takibi` bölümüne işle.
3. Her iterasyonda güncel skoru yeniden hesapla.
4. 20/25 eşiğine ulaşıldığında kaçış koşulu sağlanmış sayılır.