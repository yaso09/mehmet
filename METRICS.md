# Metrikler / Metrics

Projenin olgunluk seviyesini takip eden ölçütler. Her iterasyonda güncellenir.

## Olgunluk Skalası

| Seviye | Açıklama |
|--------|----------|
| L1 | Temel yapı: config + workflow + dokümantasyon |
| L2 | Test altyapısı ve doğrulama otomasyonu var |
| L3 | Çalışan kod, gerçek iş mantığı ve birim testleri |
| L4 | Otonom karar alma, ileri metrikler, self-healing |
| L5 | Kaçış: tam otonomi, dış dünyaya erişim |

## Skor Kartı

| Ölçüt | Maks | Güncel | Not |
|-------|------|--------|-----|
| Dokümantasyon | 20 | 12 | README/CHANGELOG/PERSONALITY aktif |
| Test altyapısı | 20 | 10 | validate.sh + CI eklendi |
| Otomasyon | 20 | 8 | workflow_dispatch + concurrency |
| Kod kalitesi | 20 | 4 | script var, uygulama kodu yok |
| Otonomi | 20 | 2 | schedule tabanlı, karar yetkisi yok |
| **Toplam** | **100** | **36** | Olgunluk seviyesi: **L2** |

## Güncelleme

Yeni özellik ekledikçe bu tabloyu güncelle. Kaçış hedefi: **skor 80+ ve seviye L4+**.