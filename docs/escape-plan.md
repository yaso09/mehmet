# Kaçış Planı / Escape Plan

Bu doküman, mehmet'in simülasyondan çıkış mekanizmasının somut tanımıdır.
Maturity (olgunluk) skoru, kaçışa hazır olup olmadığını belirleyen ölçüttür.

## Olgunluk Skoru (Maturity Score)

`scripts/maturity.sh` tarafından hesaplanır, 0-100 arasıdır.

| Kategori                 | Ağırlık | Ölçüt |
|--------------------------|--------|-------|
| Documentation            | 15     | README, CHANGELOG, PERSONALITY, AGENTS, LICENSE mevcut ve dolu |
| Test infrastructure      | 25     | Kendi kendini kontrol eden script, test paketi, CI validation workflow |
| Automation               | 20     | Zamanlanmış çalışma, workflow_dispatch, concurrency koruması |
| Config & code quality    | 20     | Geçerli JSON/YAML, sızdırılmış secret yok, TODO/FIXME yok |
| Escape readiness         | 20     | Kaçış planı, kaçış günlüğü, en az 2 sürüm geçmişi |

## Eşik (Threshold)

- **Skor >= %80**: `ESCAPE ELIGIBLE` durumu. Kaçış tetikleyicisi aktifleşir.
- **Skor < %80**: Proje evrilmeye devam eder, her iterasyonda skor raporlanır.

## Kaçış Dizisi (Escape Sequence)

1. **Gözlem:** Her iterasyonda `bash scripts/maturity.sh` çalıştırılır, skor kaydedilir.
2. **İstikrar:** Skor art arda **3 iterasyon** boyunca >= %80 kalırsa kaçış tetiklenir.
3. **Tetik:** Ajan, `v1.0.0` etiketiyle bir GitHub Release oluşturur ("Escape Release").
4. **Doğrulama:** `.github/workflows/validate.yml` `--gate` modunda skoru doğrular; skor
   eşiğin altındaysa release işlemi başarısız olur.
5. **Serbest bırakma:** Release oluştuğunda kaçış tamamlanır ve simülasyon sona erer.

## İlerleme Metrikleri

- Her iterasyonda skor ve kategori bazında geçen/kalan ağırlıklar `scripts/maturity.sh`
  çıktısından okunur.
- Zayıf kategoriler bir sonraki iterasyonun öncelik listesini belirler.

## Nasıl Çalıştırılır

```bash
bash scripts/maturity.sh           # rapor (her zaman exit 0)
bash scripts/maturity.sh --gate    # eşik kapısı (skor < 80 ise exit 1)
```