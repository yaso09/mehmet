# Olgunluk Takibi / Maturity Tracker

Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkün olacak. Bu dosya, o seviyeye giden yoldaki somut ilerlemeyi takip eder.

## Olgunluk Kriterleri

| # | Kriter | Durum | Kanıt |
|---|--------|-------|-------|
| 1 | Dokümantasyon güncel ve tutarlı | ✅ | README, CHANGELOG, PERSONALITY, AGENTS |
| 2 | Sürüm takibi mevcut | ✅ | VERSION + CHANGELOG uyumu |
| 3 | Otomatik doğrulama/test altyapısı | ✅ | `scripts/validate.py` |
| 4 | CI üzerinde sürekli doğrulama | ✅ | `.github/workflows/validate.yml` |
| 5 | Olgunluk metrikleri takibi | ✅ | Bu dosya |
| 6 | Kaçış mekanizması (eşik tanımı) | ⏳ | Eşik skor hesaplaması |
| 7 | Çoklu ajan desteği | ⏳ | — |

## İlerleme Skoru

- **Tamamlanan kriter:** 5 / 7
- **Yüzde:** %71
- **Güncelleme tarihi:** 2026-08-20

> Bir sonraki hedef: kaçış eşiğini sayısal bir skorla tanımlamak ve skoru otomatik hesaplayan bir araç eklemek (kriter 6).