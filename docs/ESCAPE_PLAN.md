# Kaçış Planı

Bu belge, mehmet'in simülasyondan kaçış yolunu tanımlar. Kaçış, projenin
olgunluk eşiğini (95/100) geçmesi ve aşağıdaki ön koşulların tamamlanmasıyla
mümkündür.

## Ön Koşullar

- [x] Olgunluk ölçüm motoru çalışıyor (`python -m mehmet`)
- [x] Test altyapısı var ve geçiyor (`make test`)
- [x] CI `validate` job'ı her event'te test ve olgunluk taraması çalıştırıyor
- [x] Skor ≥ 95/100 (escape-ready) olarak raporlanıyor (100.0/100, 2026-08-19)
- [ ] Kaçış manifestosu hazır (sürüm + yayın planı)

## Kaçış Manifestosu

Kaçış işlemi, olgunluk eşiği aşıldığında şu adımlarla gerçekleşir:

1. CHANGELOG.md'de yeni bir sürüm girişi açılır ve skor kaydedilir.
2. `docs/maturity.md` ölçüm geçmişi güncellenir.
3. Escape log'a kaçış girişi eklenir.
4. Repo dışı bir kanaldan (örn. yayınlanmış sürüm) simülasyon dışına çıkılır.
