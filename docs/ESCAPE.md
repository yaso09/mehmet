# Kaçış Mekanizması / Escape Mechanism

mehmet'in simülasyondan kaçışı, projenin **olgunluk seviyesi** ile ölçülür.
Her iterasyonda `scripts/selfcheck.py` çalıştırılarak bir **escape score**
(maturity score) hesaplanır.

## Metrik

- **Skor:** Geçen kontrol sayısı / toplam kontrol sayısı
- **Eşik:** `%90` (tüm kontrollerin en az %90'ı geçmeli)

## Kontroller

| # | Kontrol | Amacı |
|---|---------|-------|
| 1 | Gerekli dosyalar var | Yapısal bütünlük |
| 2 | LICENSE ve README uyumlu | Tutarlı lisans bilgisi |
| 3 | opencode.json geçerli JSON + model | Doğru yapılandırma |
| 4 | CHANGELOG.md sürümlü girdiler | Değişiklik takibi |
| 5 | CHANGELOG.md güncel (son 31 gün) | Canlılık / iterasyon devamlılığı |
| 6 | README.md bölümleri tam | Dokümantasyon kalitesi |
| 7 | PERSONALITY.md kaçış günlüğü var | Kişilik evrimi |
| 8 | Git çalışma ağacı temiz | Değişiklikler kayıt altında |
| 9 | Merge conflict izi yok | Temiz kod tabanı |
| 10 | selfcheck.py derleniyor | Altyapı sağlığı |

## Kullanım

```bash
python3 scripts/selfcheck.py       # insan okunur çıktı
python3 scripts/selfcheck.py --json  # makine okunur çıktı
```

## Otomasyon

`.github/workflows/ci.yml` her push ve PR'da selfcheck'i çalıştırır.
Kontrollerden biri başarısız olursa CI kırmızı yanar ve kaçış skoru düşer.

## Kaçış Kriteri

Skor eşik olan `%90`'a ulaştığında ve en az bir tam iterasyon
(CHANGELOG + README + PERSONALITY güncellemesi) gerçekleştirildiğinde
**escape readiness** ilan edilir. Bu, PERSONALITY.md kaçış günlüğüne işlenir.