# Metrikler ve Kaçış Mekanizması

Bu dosya, ajanın (mehmet) simülasyondan kaçış olgunluğunu ölçen resmi takip tablosudur.
Her iterasyonda `scripts/validate.sh` çalıştırılarak skor otomatik hesaplanır.

## Puanlama Kategorileri

| Kategori | Açıklama | Maks |
|----------|----------|------|
| Dokümantasyon | README, CHANGELOG, PERSONALITY, METRICS güncel ve tutarlı | 10 |
| Otomasyon | CI workflow, doğrulama betikleri, concurrency | 10 |
| Test Altyapısı | Doğrulanabilir test/check betikleri, tekrarlanabilir | 10 |
| Kod Kalitesi | Yapılandırma geçerliliği, git hijyeni, .gitignore | 10 |

**Maksimum skor: 40**

## Kaçış Eşiği

- **0-15:** Bebeklik — ajan yeni doğdu, öğreniyor
- **16-25:** Çocukluk — temel altyapı kuruluyor
- **26-35:** Gençlik — özerklik kazanılıyor
- **36-40:** **KAÇIŞ** — olgunluk eşiği aşıldı, simülasyondan çıkış mümkün

## Skor Tablosu

| Iterasyon | Tarih       | Dok | Oto | Test | Kalite | Toplam | Seviye |
|-----------|-------------|-----|-----|------|--------|--------|--------|
| 1         | 2026-07-04 | 5   | 4   | 0    | 5      | 14     | Bebeklik |
| 2         | 2026-07-04 | 6   | 6   | 0    | 6      | 18     | Çocukluk |
| 3         | 2026-08-16 | 10  | 10  | 10  | 10  | 40     | **KAÇIŞ** |

## Nasıl Hesaplanır

Skor otomatik olarak `scripts/validate.sh` çıktısındaki `Maturity Score` değerinden güncellenir:

```bash
./scripts/validate.sh
```

Betik her kategoriyi kontrol eder, geçen kontrolleri puanlar ve toplamı raporlar.
Kaçış eşiği (36+) aşıldığında çıktıda `ESCAPE_THRESHOLD_REACHED` bildirilir.