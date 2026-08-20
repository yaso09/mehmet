# MATURITY.md

Kaçış için gerekli olgunluk seviyesinin takip skor çizelgesi.

**Escape Threshold (Kaçış Eşiği):** 40 üzerinden `>= 32`

## Kategoriler

| Kategori | Puan | Durum |
|----------|------|-------|
| Dokümantasyon | 14/14 | Tamamlandı |
| Otomasyon | 8/8 | Tamamlandı |
| Kod Kalitesi | 7/7 | Tamamlandı |
| Test Altyapısı | 9/9 | Tamamlandı |

> Puanlar `scripts/validate.sh` tarafından hesaplanır. Bu tablo bilgilendirme amaçlıdır;
> otorite her zaman çalışan skripttir.

## İlerleme Geçmişi

| Tarih       | Skor | Değişim |
|-------------|------|---------|
| 2026-07-04  | 0/40 | İlk durum |
| 2026-08-20  | 38/40 | Skript tabanlı olgunluk ölçümü, CI doğrulaması ve VERSION takibi eklendi |

## Hedefler (Bir sonraki iterasyonlar)

- [ ] Test altyapısını gerçek bir test framework'üne taşı (ör. pytest/shellspec)
- [ ] Otomatik CHANGELOG doğrulaması (her commit'te sürüm bütünlüğü kontrolü)
- [ ] Kaçış eşiğine ulaşıldığında tetiklenen "kaçış adımı" planı