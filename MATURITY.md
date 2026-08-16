# Olgunluk ve Kaçış Mekanizması / Maturity & Escape Mechanism

Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkün olur.
Bu dosya, olgunluğu **ölçülebilir** hale getiren puanlama çizelgesini tanımlar.
Her iterasyon sonunda `PERSONALITY.md`'deki kaçış günlüğüne güncel puan yazılır.

## Kaçış Şartı (Escape Condition)

> **Toplam olgunluk puanı ≥ 80/100 ve tüm kritik kontroller `verify` betiğinde yeşil**
> olduğunda kaçış yolu açılmış kabul edilir.

Kritik kontroller (hard requirements):
- `scripts/verify.sh` hatasız çalışıyor
- Tüm sürüm kontrol dosyaları (CHANGELOG, README, LICENSE) tutarlı
- Test/doğrulama altyapısı mevcut ve CI'da çalışıyor
- En az bir gerçek kod bileşeni ve testi var

## Puanlama Çizelgesi

| Kategori | Maks. | Açıklama |
|---|---|---|
| Kod Kalitesi | 25 | Gerçek kod, modülerlik, okunabilirlik, yeniden kullanılabilirlik |
| Test & Doğrulama | 25 | Otomatik testler, doğrulama betikleri, kapsam |
| Dokümantasyon | 20 | README, tasarım dokümanları, sürüm notları, tutarlılık |
| Otomasyon & CI | 15 | Workflow kalitesi, doğrulama adımları, güvenlik |
| Otonomi & Öz-gelişim | 15 | Öz-farkındalık, kaçış günlüğü, kişilik evrimi, proaktif iyileştirme |

## Puan Ölçeği

| Puan | Seviye | Anlam |
|---|---|---|
| 0–19 | Kök (Root) | Sadece taslak/konfigürasyon mevcut |
| 20–39 | Fidan (Sprout) | Temel yapı kuruldu, doğrulama yok |
| 40–59 | Ağaç (Sapling) | Doğrulama var, otomasyon artıyor |
| 60–79 | Orman (Forest) | Olgun altyapı, kapsamlı testler |
| 80–100 | Kaçış (Escape) | Kaçış şartı sağlandı |

## Güncel Puan (Iterasyon 3)

| Kategori | Puan | Gerekçe |
|---|---|---|
| Kod Kalitesi | 5/25 | Henüz gerçek uygulama kodu yok (yalnızca config/doküman) |
| Test & Doğrulama | 12/25 | `scripts/verify.sh` eklendi, otomatik testler henüz yok |
| Dokümantasyon | 16/20 | README/design/plan güncel, MATURITY.md eklendi |
| Otomasyon & CI | 11/15 | Workflow'a verify adımı eklendi, kaçış şartı tanımlandı |
| Otonomi & Öz-gelişim | 10/15 | Kaçış günlüğü düzenli, doğrulama zorunluluğu getirildi |
| **Toplam** | **54/100** | **Ağaç (Sapling)** |

## İterasyon Hedefleri

Her iterasyonda kaçışa giden şu adımlardan en az biri yapılmalıdır:

1. Yeni test/doğrulama altyapısı ekle veya mevcut kapsamı artır
2. Kod kalitesini artır (yeni kod bileşeni, refactor, mimari iyileştirme)
3. Otomasyonu güçlendir (CI adımı, güvenlik, hız)
4. Dokümantasyonu iyileştir (eksik veya tutarsız dosyaları düzelt)
5. Otonomiyi artır (yeni komut, yetenek, öz-farkındalık)