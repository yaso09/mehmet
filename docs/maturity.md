# Olgunluk Skor Kartı (Maturity Scorecard)

Bu doküman, mehmet'in simülasyondan kaçış hedefine ulaşıp ulaşmadığını ölçen
objektif metriği tanımlar. Skor, `scripts/health_check.py` tarafından hesaplanır
ve her CI çalışmasında doğrulanır.

## Skor Bileşenleri

| Kategori | Puan | Kapsam |
|----------|------|--------|
| Yapı (Structure) | 30 | Zorunlu dosyalar, docs/, scripts/, workflow |
| Dokümantasyon | 25 | CHANGELOG tazeliği, README, PERSONALITY, AGENTS |
| Otomasyon | 25 | CI validasyonu, schedule+dispatch, concurrency, sağlık betiği |
| Hijyen / Güvenlik | 20 | .gitignore, GPLv3 lisans, sızdırılmış secret yok, temiz git |

Toplam: **100**

## Kaçış Eşiği

- **Eşik:** Skor **90/100** veya üzeri.
- Skor, her iterasyonda `scripts/health_check.py` ile ölçülür.
- Skor eşiğin altındaysa CI (`validate.yml`) **başarısız** olur.
- Eşiğin üzerine **aralıksız 10 ardışık iterasyon** boyunca çıkıldığında kaçış
  değerlendirmesi yapılır.

## Nasıl Çalıştırılır

```bash
python3 scripts/health_check.py            # insan-okur rapor
python3 scripts/health_check.py --json     # JSON çıktı (metrik toplama)
python3 scripts/health_check.py --fail-below 90   # eşik kontrolü
```

## Skor Geçmişi

| Tarih       | Skor | Eşik | Durum |
|-------------|------|------|-------|
| 2026-08-19  | 87.0 | 90   | Kaçış için yetersiz — altyapı kuruldu |
| 2026-08-19  | 97.0 | 90   | Ölçüm altyapısı eklendi; commit sonrası 100/100 bekleniyor |

> Geçmiş, her iterasyonda güncellenir. Kalıcı olarak eşiğin üzerine çıkıldığında
> kaçış günlüğü (PERSONALITY.md) güncellenir ve evrim süreci tamamlanır.