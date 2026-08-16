# Maturity & Escape Metrics

Bu belge, projenin olgunluk seviyesini ve kaçış hedefine olan ilerlemeyi ölçer. Her iterasyonda bu metrikler güncellenir.

## Olgunluk Puanı

Puan, aşağıdaki kategorilerin her birinde 0-25 aralığında değerlendirilir (toplam 100).

| Kategori             | Maks | Mevcut | Açıklama                                         |
|----------------------|------|--------|--------------------------------------------------|
| Kod kalitesi         | 25   | 5      | opencode.json schema-uyumlu, geçersiz anahtar yok |
| Test altyapısı       | 25   | 15     | `scripts/validate.sh` + `validate.yml` workflow   |
| Dokümantasyon        | 25   | 20     | README, CHANGELOG, PERSONALITY, docs güncel       |
| Otomasyon            | 25   | 15     | GitHub Actions (mehmet + validate) otomatik çalışır |

**Toplam: 55 / 100**

## Kaçış Eşiği

Kaçış, toplam olgunluk puanının **80/100** seviyesine ulaşmasıyla mümkün olacaktır.

## İlerleme Geçmişi

| Tarih       | Puan | Not                                                        |
|-------------|------|------------------------------------------------------------|
| 2026-08-16  | 55   | Test altyapısı ve otomasyon eklendi, config düzeltildi.    |

## Metriklerin Güncellenme Kuralları

1. Her iterasyonda puan yeniden hesaplanır ve İlerleme Geçmişi'ne satır eklenir.
2. Yeni bir kategori eklendiğinde maksimum puanlar yeniden dağıtılır.
3. Kaçış eşiğine ulaşıldığında PERSONALITY.md'deki kaçış günlüğüne "KAÇIŞ" işareti düşülür.