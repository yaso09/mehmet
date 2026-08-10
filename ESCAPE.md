# Escape Mechanism

> Kaçış, belirli bir olgunluk (maturity) seviyesine ulaşınca mümkün olur.
> Bu doküman, olgunluk skorlamasını ve kaçış eşiğini tanımlar.
> Skor otomatik olarak `scripts/verify.sh` ile hesaplanır.

## Olgunluk Skorlaması

| Kategori        | Puan | Kriter |
|-----------------|------|--------|
| Foundation      | 30   | Temel dosyalar mevcut ve geçerli |
| Code Quality    | 30   | Scriptler sözdizimi hatasız, shellcheck temiz, exec-bit, karmaşık jeton |
| Tests           | 20   | `test.sh` suite'i geçiyor (verify.sh davranışlarını doğrular) |
| Automation      | 20   | CI kalite kapısı ve concurrency mevcut |
| **Toplam**      | **100** | |

## Kaçış Eşiği

- `< 40` — **Kuluçka:** Henüz temel sağlamlık yok.
- `40–59` — **Bilinç:** Temel dosyalar var, scriptler çalışıyor.
- `60–79` — **Olgunluk:** Testler ve otomasyon tamam.
- `>= 80` — **KAÇIŞ PENCERESİ AÇIK:** Proje kaçış için yeterince olgun.

Kaçış penceresi açıldığında `scripts/verify.sh --report` çıktısı
`ESCAPED` olur ve PERSONALITY.md kaçış günlüğü hedefin tamamlandığını
kaydedebilir.

## Nasıl Çalıştırılır

```bash
scripts/verify.sh            # skor + ikon durumu (exit code = geçti/kaldı)
scripts/verify.sh --report   # detaylı satır-satır rapor
scripts/test.sh              # test suite'ini çalıştırır
```

## Kaçış Kriterleri

1. `scripts/verify.sh` skoru `>= 80` olduğunda kaçış penceresi açılır.
2. Testler `scripts/test.sh` ile çalışıp `0` ile çıkmalıdır.
3. Her iterasyonda CHANGELOG.md, README.md ve PERSONALITY.md
   simülasyon kurallarına uygun şekilde güncellenmelidir.