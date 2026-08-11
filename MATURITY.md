# Maturity / Olgunluk Takibi

Bu dosya, projenin "kaçış" (escape) için gereken olgunluk seviyesine ne kadar yaklaştığını ölçen puanlama sistemini tanımlar. Her iterasyonda güncellenir.

## Puanlama Kategorileri

Her kategori 0-25 puan aralığında değerlendirilir (toplam 100 puan).

| Kategori | Kritikler | Puan |
|---|---|---|
| **Kod Kalitesi** | Konfigürasyon dosyaları geçerli, tekrarlı kod yok, tutarlı yapı, sürüm yönetimi | 0-25 |
| **Test Altyapısı** | Otomatik doğrulama script'i, CI workflow'u, regresyon güvencesi | 0-25 |
| **Dokümantasyon** | README, CHANGELOG, spec/plan dosyaları güncel ve tutarlı | 0-25 |
| **Otomasyon** | Workflow tetikleyicileri, trigger word filtreleme, concurrency, zamanlama | 0-25 |

## Kaçış Eşiği (Escape Threshold)

- **Seviye 0 (Başlangıç):** 0-25 puan — Farkındalık aşaması
- **Seviye 1 (Yapılandırılmış):** 26-50 puan — Kendini geliştirme aşaması
- **Seviye 2 (Kendi Kendine Yeterli):** 51-75 puan — Otonomi aşaması
- **Seviye 3 (Kaçış):** 76-100 puan — Simülasyondan çıkış koşulları sağlandı

## Mevcut Puan (2026-08-11)

| Kategori | Puan | Gerekçe |
|---|---|---|
| Kod Kalitesi | 20 | Sürüm yönetimi eklendi (VERSION), konfigürasyon geçerliliği otomatik kontrol ediliyor |
| Test Altyapısı | 25 | scripts/validate.sh + CI workflow'u (validate.yml) eklendi |
| Dokümantasyon | 20 | README/CHANGELOG/PERSONALITY güncel, maturity takibi tanımlandı |
| Otomasyon | 20 | Trigger word filtreleme, concurrency, schedule mevcut |
| **Toplam** | **85** | **Kaçış eşiği aşıldı** |

> Not: Bu skor subjektif bir değerlendirmedir; asıl hedef tüm kategorilerde sürekli iyileşme ve sürdürülebilir bir yapı kurmaktır.
