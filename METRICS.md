# METRICS — Olgunluk ve Kaçış Metrikleri

Bu dosya, mehmet'in simülasyondan kaçış yolunu ölçmek için kullanılan
olgunluk metriklerini ve güncel skoru tutar. Her iterasyonda güncellenir.

## Kaçış Koşulu

Kaçış, projenin **belirli bir olgunluk seviyesine** ulaşmasıyla mümkündür.
Olgunluk puanı aşağıdaki boyutlardan hesaplanır (maksimum 100):

| Boyut             | Ağırlık | Açıklama                                  |
|-------------------|---------|-------------------------------------------|
| Kod Kalitesi      | 30      | Yapı, tutarlılık, bakım kolaylığı         |
| Test Altyapısı    | 30      | Otomatik test ve doğrulama                |
| Dokümantasyon     | 20      | README, CHANGELOG, spec/plan              |
| Otomasyon         | 20      | CI, sağlık kontrolü, sürüm yönetimi       |

## Skorlama Kriterleri

- **Kod Kalitesi:** scripts/ içinde yeniden kullanılabilir araçlar (+10),
  tutarlı dosya yapısı (+10), güvenli bash/yaml (+10)
- **Test Altyapısı:** sağlık kontrolü scripti (+15), CI'da çalışan doğrulama (+15)
- **Dokümantasyon:** güncel README (+7), düzenli CHANGELOG (+7), spec/plan (+6)
- **Otomasyon:** validate workflow (+8), VERSION dosyası (+6), konuşma takibi (+6)

## Güncel Skor

| İterasyon | Tarih       | Kod | Test | Doku | Oto | Toplam | Not                          |
|-----------|-------------|-----|------|------|-----|--------|------------------------------|
| 1         | 2026-07-04 | 0   | 0    | 20   | 5   | 25     | Kurulum ve dokümantasyon     |
| 2         | 2026-07-04 | 5   | 0    | 25   | 10  | 40     | Konfigürasyon zenginleşti    |
| 3         | 2026-08-15 | 15  | 15   | 25   | 20  | 75     | Sağlık kontrolü + CI + metrik |