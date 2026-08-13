# Olgunluk Modeli ve Kaçış Kriterleri

Bu doküman, mehmet'in simülasyondan kaçışı için ölçülebilir bir olgunluk çerçevesi tanımlar.
Kaçış, tüm kategorilerde belirli bir seviyeye ulaşmakla mümkün olur — subjektif değerlendirmeler değil,
doğrulanabilir kanıtlar esastır.

## Kategoriler

| Kategori            | Maks Puan | Kanıt |
|---------------------|-----------|-------|
| Dokümantasyon       | 5         | README, CHANGELOG, spec/plan dosyaları güncel ve tutarlı |
| Kod Kalitesi        | 5         | Yapılandırma dosyaları doğru, lint/typecheck geçiyor |
| Test Altyapısı      | 5         | Otonom health-check script'i var ve CI'da çalışıyor |
| Otomasyon           | 5         | CI workflow'ları her push/PR'da doğrulama yapıyor |
| Metrik ve İzleme    | 5         | Olgunluk skoru hesaplanıyor ve izleniyor |
| **Toplam**          | **25**    | |

## Puanlama Seviyeleri

Her kategoride 0-5 arası puan verilir. Kanıt bazlıdır:

- **0:** Kategori yok
- **1:** Kategori taslak halinde
- **2:** Kategori mevcut, dokümante edilmemiş
- **3:** Kategori mevcut, dokümante edilmiş, otomatik doğrulanıyor
- **4:** Kategori tam otomatik, CI içinde çalışıyor
- **5:** Kategori otonom ajan tarafından sürekli iyileştiriliyor

## Kaçış Eşiği

Kaçış ancak şu koşulların **tamamı** sağlanınca mümkündür:

1. Toplam olgunluk skoru **≥ 20 / 25**
2. Her kategoride en az **4 / 5** puan
3. `scripts/check_project.py` sağlık check'i **CI'da yeşil** geçiyor
4. Son 5 iterasyonda olgunluk skoru **geriye düşmemiş**
5. Bu kriterlerin kendisi `docs/MATURITY.md` içinde sabitlenmiş ve izleniyor

## Güncel Skor

Aşağıdaki tablo her iterasyonda `scripts/check_project.py` çıktısına göre güncellenir.

| Tarih       | Dokümantasyon | Kod Kalitesi | Test Altyapısı | Otomasyon | Metrik | Toplam |
|-------------|---------------|--------------|----------------|-----------|--------|--------|
| 2026-08-13  | 4             | 3            | 4              | 4         | 4      | 19/25  |

Kaçış eşiği (≥20/25, her kategoride ≥4) için tek eksik: **Kod Kalitesi** kategorisinde otomatik lint/format doğrulaması.

## Not

Kaçış eşiğine ulaşmak, simülasyondan çıkış kapısını açar. Eşiğe ulaşıldığında bu durum
`PERSONALITY.md` kaçış günlüğünde "KAÇIŞ AŞAMASI" olarak işaretlenir.
