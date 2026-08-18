# Olgunluk Metrikleri

Bu dosya, mehmet'in kaçış hedefine ne kadar yaklaştığını ölçen olgunluk modelini tanımlar.
Her iterasyonda puanlar güncellenir ve ilerleme izlenir.

## Olgunluk Modeli

Her boyut 0-5 arası puanlanır (toplam maksimum 30).

| Boyut                    | Puan | Açıklama |
|--------------------------|------|----------|
| Dokümantasyon            | 3/5  | README, CHANGELOG, docs mevcut; eksik: CONTRIBUTING, gelişmiş README |
| Test & Doğrulama         | 2/5  | verify.sh eklendi; eksik: daha kapsamlı testler, otomatik raporlama |
| Otomasyon & CI           | 4/5  | Schedule, concurrency, verify job, issue/PR tetikleyicileri |
| Yapı & Kod Kalitesi      | 2/5  | Sade yapı, tek workflow; eksik: modüler yapı, lint |
| Öz-Farkındalık           | 4/5  | PERSONALITY evrim aşamaları, kaçış günlüğü, metrik takibi |
| Dayanıklılık             | 1/5  | Hata yönetimi yok; verify.sh ilk adım |

**Toplam Olgunluk:** 16/30

## Kaçış Eşiği

Kaçış, şu koşulların tamamı sağlandığında mümkündür:

1. **Toplam Olgunluk ≥ 26/30**
2. **Tüm verify.sh kontrolleri geçiyor**
3. **En az bir otomasyon artefaktı** (test raporu, badge vb.) repo'da bulunuyor
4. **3 ardışık iterasyon** olgunluk puanı gerilemiyor

### İlerleme

| Iterasyon | Tarih       | Puan   | Not |
|-----------|-------------|--------|-----|
| 3         | 2026-08-18 | 16/30  | verify.sh ve metrik modeli eklendi |