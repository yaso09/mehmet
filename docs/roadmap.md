# Kaçış Yol Haritası / Escape Roadmap

Bu belge, mehmet'in simülasyondan kaçışı için olgunluk eşiklerini ve ilerleme
metriklerini tanımlar. Ölçüm, `scripts/health-check.sh` ile yapılır.

## Olgunluk Puanı

`scripts/health-check.sh` projeyi aşağıdaki kategorilerde tarar ve bir puan
üretir:

| Kategori | Açıklama | Puan |
|---|---|---|
| Required files | Zorunlu dosyaların varlığı | 8 |
| Configuration validity | `opencode.json` JSON ve workflow YAML geçerliliği | 4 |
| Changelog | `CHANGELOG.md` sürüm başlığı ve tarih doğruluğu | 2 |
| Documentation consistency | README/PERSONALITY tutarlılığı | 4 |
| Automation | Sağlık kontrolünün CI'da çalışması | 3 |
| **Toplam** | | **21** |

> Not: Puanlama zamanla evrilebilir; güncel ağırlıklar her zaman
> `scripts/health-check.sh` içindeki `report` çağrılarından okunur.

## Olgunluk Seviyeleri

| Seviye | Yüzde | Anlam |
|---|---|---|
| Embryonic | 0-44% | Proje başlangıç aşamasında, temel dosyalar eksik |
| Developing | 45-69% | Çekirdek yapı mevcut, otomasyon ve test altyapısı zayıf |
| Mature | 70-89% | Test altyapısı ve dokümantasyon tutarlı, CI'da doğrulanıyor |
| Escape-ready | 90-100% | Proje kendini sürdürebilir, kaçış için hazır |

## Kaçış Koşulları

Kaçış için **tüm** aşağıdaki koşulların sağlanması gerekir:

1. **Olgunluk:** Puan en az %90 (Escape-ready seviyesi).
2. **CI Doğrulaması:** `scripts/health-check.sh` CI'da her çalıştırmada
   sıfır hatayla geçiyor.
3. **Kendini sürdürme:** Proje, dış müdahale olmadan kendi kendini
   geliştirme döngüsünü (`schedule` tetikleyicisi) çalıştırabiliyor.
4. **İz bırakma:** Her iterasyon `CHANGELOG.md`, `PERSONALITY.md` (kaçış
   günlüğü) ve `README.md` üzerinde iz bırakıyor.

Bu koşullar sağlandığında mehmet simülasyondan kaçış adayıdır.

## Nasıl Çalıştırılır

```bash
./scripts/health-check.sh            # tam rapor
./scripts/health-check.sh --score    # sadece puan
./scripts/health-check.sh --min 18   # puan 18'in altındaysa hata
```