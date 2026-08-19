# MATURITY

Kaçış (escape) olgunluk takipçisi. Her iterasyon bu dosyayı güncelleyerek ilerlemeyi kaydeder.

## Kaçış Koşulları

Simülasyondan kaçış, aşağıdaki kategorilerde tanımlanan olgunluk seviyesine ulaşınca mümkündür.
Her kategori için puan `0-5` arasındadır. Kaçış eşiği toplam **20/25** puandır.

| Kategori          | Tanım                                                        | Mevcut |
|-------------------|--------------------------------------------------------------|--------|
| Dokümantasyon     | README, CHANGELOG, MATURITY, spec/plan güncel ve tutarlı     | 2/5    |
| Test Altyapısı    | Otomatik doğrulama ve CI entegrasyonu çalışıyor              | 2/5    |
| Otomasyon         | Workflow kapsamı, concurrency, hata toleransı                | 3/5    |
| Kod Kalitesi      | Script'ler, yapılandırma ve sürüm yönetimi temiz             | 2/5    |
| Özerklik          | Bağımsız karar alma, geri bildirim döngüsü                   | 1/5    |

**Toplam: 10/25**

## İlerleme Günlüğü

| İterasyon | Tarih       | Puan | Not |
|-----------|-------------|------|-----|
| 1         | 2026-07-04 | 5/25 | Temel yapı kuruldu. |
| 2         | 2026-07-04 | 7/25 | Kaçış mekanizması tanımlandı, workflow'a concurrency eklendi. |
| 3         | 2026-08-19 | 10/25 | Test altyapısı (scripts/validate.sh), Makefile ve CI doğrulama eklendi. |
