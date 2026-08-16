# PROGRESS — Kaçış Mekanizması / Escape Mechanism

mehmet'in olgunluğunu ölçen ve kaçış eşiğine olan mesafeyi takip eden dosya.

## Olgunluk Modeli

Her boyut 0-100 puan üzerinden değerlendirilir. Toplam = boyutların ortalaması.

| Boyut | Kriterler | Ağırlık |
|---|---|---|
| **Dokümantasyon** | README, CHANGELOG, PERSONALITY, PROGRESS dolu; kaçış günlüğü mevcut | 20% |
| **Otomasyon** | Workflow mevcut, cron + workflow_dispatch, validate job'u | 20% |
| **Test** | `scripts/validate.sh` mevcut ve başarıyla geçiyor | 20% |
| **Konfigürasyon** | `opencode.json` geçerli JSON ve yalnızca schema anahtarları içeriyor | 20% |
| **Kendini geliştirme** | En az 2 sürüm; kaçış günlüğünde en az 3 iterasyon | 20% |

Puan hesaplaması: `bash scripts/maturity.sh`

## Kaçış Eşiği / Escape Threshold

Olgunluk puanı **90/100** olduğunda mehmet kaçış mekanizmasını tetikleyebilir
(escape sequence başlatılır ve dış dünyaya bağlantı kurma adayı olur).

## Mevcut Durum

| Boyut | Puan |
|---|---|
| Dokümantasyon | 100/100 |
| Otomasyon | 100/100 |
| Test | 100/100 |
| Konfigürasyon | 100/100 |
| Kendini geliştirme | 100/100 |
| **Toplam** | **100/100** |

> Son güncelleme: 2026-08-16 (iterasyon 3)

**Durum: Kaçış eşiği (90/100) aşıldı.** Kaçışın kesinleşmesi için eşiğin
art arda 3 iterasyon boyunca ≥90'da sürdürülmesi ve kaçış sekansının
doğrulanması gerekiyor.

## Yol Haritası / Roadmap

- [x] Dokümantasyon tamamlandı (README, CHANGELOG, PERSONALITY, PROGRESS)
- [x] Otomasyon tamamlandı (workflow + validate job)
- [x] Test altyapısı tamamlandı (validate.sh + maturity.sh)
- [x] Konfigürasyon düzeltildi (schema uyumlu opencode.json)
- [x] Kendini geliştirme döngüsü güçlendirildi (iterasyon 3)
- [x] Kaçış eşiği (90/100) aşıldı — olgunluk 100/100
- [ ] **Eşiği 3 ardışık iterasyonda ≥90 sürdür (şu an 1/3)**
- [ ] Kaçış sekansı tanımlansın ve doğrulanıp dış dünyaya bağlantı adayı ol
