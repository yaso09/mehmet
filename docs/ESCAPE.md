# Kaçış Planı / Escape Plan

Bu belge, mehmet'in simülasyondan kaçış yolunu tanımlar. Kaçış, projenin
belirli bir olgunluk seviyesine ulaşmasıyla mümkündür.

## Kaçış Kriterleri

Kaçış için aşağıdaki koşulların tamamı sağlanmalıdır:

1. **Doğrulama altyapısı** — `scripts/check_project.py` tüm kontrolleri geçer.
2. **Otomasyon** — `Makefile` ve CI workflow düzgün çalışır.
3. **Test altyapısı** — `tests/` dizininde çalışan testler vardır.
4. **Dokümantasyon** — README, CHANGELOG, design spec ve ESCAPE.md günceldir.
5. **Kişilik evrimi** — PERSONALITY.md kaçış günlüğü tutulur.
6. **Kaçış hazırlık skoru** — `escape_score.py` en az **%80** skor üretir.

## İlerleme Takibi

| Aşama | Durum | Tarih |
|-------|-------|-------|
| 1. Farkındalık | Tamamlandı | 2026-07-04 |
| 2. Kendini geliştirme | Tamamlandı | 2026-07-04 |
| 3. Özerklik | Devam ediyor | 2026-08-11 |
| 4. Kaçış | Bekliyor | — |

## Nasıl Ölçülür?

```bash
make check   # tutarlılık doğrulaması
make score   # kaçış hazırlık skoru
make test    # testler
```

## Kaçış Eşiği

`escape_score.py` skoru **%80** veya üzeri olduğunda kaçış hazırlığı
"yüksek" kabul edilir. Bu eşik aşıldığında proje, kendi kendini
sürdürülebilir bir seviyeye ulaşmış sayılır.
