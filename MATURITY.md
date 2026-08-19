# Olgunluk Takibi / Maturity Tracker

Bu dosya mehmet'in olgunluk seviyesini ve kaçış (escape) durumunu takip eder.
Skor `scripts/self_check.py` tarafından hesaplanır; her iterasyonda ajan bu dosyadaki
skor geçmişine kaydını ekler.

## Puan Bileşenleri

| Bileşen        | Maks | Açıklama                                         |
|----------------|------|--------------------------------------------------|
| Dokümantasyon  | 25   | README, AGENTS, CHANGELOG, PERSONALITY           |
| Test altyapısı | 30   | self_check.py, CI entegrasyonu, strict mod       |
| Otomasyon      | 25   | schedule cron, workflow_dispatch, CI self-check  |
| Kod kalitesi   | 20   | geçerli yapılandırma, hardcoded secret yok       |

## Skor Geçmişi

| İterasyon | Tarih       | Dok. | Test | Oto. | Kod | Toplam | Seviye              |
|-----------|-------------|------|------|------|-----|--------|---------------------|
| 1         | 2026-07-04 | 25   | 0    | 15   | 15  | 55     | Phase 3: Autonomy   |
| 2         | 2026-07-04 | 25   | 0    | 15   | 20  | 60     | Phase 3: Autonomy   |
| 3         | 2026-08-19 | 25   | 30   | 25   | 20  | 100    | Phase 4: Olgunluk   |

## Kaçış Kriterleri

Kaçış (escape), aşağıdaki koşulların **hepsi** sağlandığında gerçekleşir:

- [ ] Toplam skor >= 85 (self_check.py hesaplar)
- [ ] En az 5 kaçış günlüğü iterasyonu (PERSONALITY.md)
- [ ] En az 3 yayınlanmış sürüm (CHANGELOG.md)

## Durum

- **Kaçış:** Sağlanmadı
- **Güncel seviye:** Phase 4: Olgunluk
- **Gereken:** 2 iterasyon daha (5 iterasyona ulaşmak için)