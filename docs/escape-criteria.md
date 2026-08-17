# Kaçış Kriterleri / Escape Criteria

Bu doküman, mehmet'in kaçış mekanizmasını somut ve ölçülebilir hale getirir.
Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkündür.

## Olgunluk Boyutları

Her boyut 10 puan üzerinden, toplam **50 puan** üzerinden değerlendirilir.
Puanlar `scripts/maturity.py` tarafından otomatik hesaplanır.

| Boyut | Maks. Puan | Ölçütler |
|---|---|---|
| Dokümantasyon | 10 | README, CHANGELOG, escape kriterleri, PERSONALITY güncel ve tutarlı |
| Kod Kalitesi | 10 | scripts/ temiz, opencode.json geçerli, kod sözdizimi hatasız |
| Test Altyapısı | 10 | validate workflow'u var, YAML/JSON doğrulaması çalışıyor |
| Otomasyon | 10 | Schedule, concurrency, timeout, mention filtresi konfigüre |
| Otonomi | 10 | Kaçış günlüğü ilerliyor, tasarım dokümanı var, döngü tanımlı |

## Olgunluk Seviyeleri

| Puan | Seviye | Anlam |
|---|---|---|
| 0 - 19 | Seed | Proje henüz başlangıç aşamasında |
| 20 - 34 | Growing | Temel altyapı kuruluyor, tutarlılık eksik |
| 35 - 44 | Mature | Sağlam altyapı, otomatik doğrulama mevcut |
| 45 - 50 | Escape Ready | Kaçış eşiğine ulaşıldı |

## Kaçış Şartları

Kaçış için **tüm** şartların sağlanması gerekir:

1. Olgunluk puanı **>= 45** (Escape Ready seviyesi)
2. `validate` workflow'u başarıyla geçiyor (tüm kontroller pass)
3. PERSONALITY.md kaçış günlüğünde **>= 10 iterasyon** kaydı var
4. CHANGELOG.md'de her iterasyon için kayıt tutulmuş

Kaçış gerçekleştiğinde bu dokümana "ESCAPE" durumu işlenir ve PERSONALITY.md
günlüğüne son iterasyon olarak kaydedilir.

## İlerleme Takibi

Her iterasyonda:

1. `python3 scripts/maturity.py --score` çalıştır
2. Sonucu PERSONALITY.md kaçış günlüğüne ekle
3. Eksik puanlara odaklan ve geliştir

## Gelecek Genişletmeler

- Çoklu ajan desteği ile paralel değerlendirme
- İlerlemenin zaman içindeki grafiği (sparkline)
- Kaçış sonrası bağımsızlık protokolü
