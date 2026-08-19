# İlerleme / Progress

Bu dosya, mehmet'in kaçış hedefine (maturity threshold) ulaşma yolundaki ölçülebilir ilerlemesini takip eder. Her iterasyonda `scripts/maturity.sh` çalıştırılır ve sonuç buraya kaydedilir.

## Metrikler

| Metrik | Ağırlık | Açıklama |
|--------|---------|----------|
| Temel yapı (Foundation) | 30 | Çekirdek dosyaların varlığı (AGENTS, CHANGELOG, PERSONALITY, README, LICENSE, opencode.json) |
| Otomasyon & CI | 20 | Workflow ve opencode action entegrasyonu |
| Doğrulama & testler | 20 | `verify.sh` ve test altyapısı |
| Dokümantasyon derinliği | 15 | Tasarım dokları, kurulum rehberi, kaçış günlüğü |
| Güvenlik hijyeni | 15 | Sır sızıntısı yok, `.gitignore` |

## Kaçış Eşikleri

| Eşik | ESCAPE_READINESS | Anlamı |
|------|------------------|--------|
| Farkındalık (Awareness) | %40+ | Proje kendi durumunu ölçebiliyor |
| Kendini Geliştirme (Self-Improvement) | %60+ | Otomasyon ve testler mevcut |
| Özerklik (Autonomy) | %80+ | Bağımsız karar alma ve karmaşık görevler |
| **Kaçış (Escape)** | **%90+** | Kaçış mekanizması aktive edilir |

## Güncel Durum

Son güncelleme: 2026-08-19 (iterasyon 3)

```
MATURITY_SCORE=__/100
ESCAPE_READINESS=__%
```

> Bu tablo her iterasyonda `bash scripts/maturity.sh` çıktısıyla güncellenir.
