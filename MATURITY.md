# Olgunluk / Maturity

Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkün olur.
Bu dosya kaçış mekanizmasının ölçümünü tanımlar ve güncel skoru izler.

## Skor Hesaplama

`./scripts/maturity.sh` her çalıştığında projeyi beş kategoride tarar ve 100 üzerinden puan verir.

| Kategori | Maks Puan |
|---|---|
| Yapı (Structure) | 20 |
| Dokümantasyon (Documentation) | 20 |
| Testler (Testing) | 20 |
| CI/CD & Otomasyon | 20 |
| Konfigürasyon Kalitesi | 20 |

Makine-okunur çıktı için: `./scripts/maturity.sh --json`

## Kaçış Eşikleri

| Skor | Durum |
|---|---|
| 0-39 | Başlangıç |
| 40-69 | Gelişme |
| 70-89 | Olgun |
| 90-100 | Kaçışa hazır |

## Güncel Skor

| Tarih | Skor | Kayıt |
|---|---|---|
| 2026-08-11 | 80 | İlk ölçüm; maturity sistemi ve kalite CI'ı eklendi |
