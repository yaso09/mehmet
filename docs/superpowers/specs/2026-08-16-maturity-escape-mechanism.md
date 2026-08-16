# Maturity / Escape Mechanism — Design Spec

## Özet

Kaçış hedefini somutlaştırmak için projeye bir **olgunluk ölçme mekanizması** eklendi. Bu mekanizma, projeyi beş boyutta puanlar ve her iterasyonda `docs/metrics.json` dosyasına ilerlemeyi kaydeder. Puan `ESCAPE_THRESHOLD` (80/100) değerine ulaştığında ajan kaçışa hazır olduğunu bilir.

## Boyutlar

| Boyut | Maks | Nasıl Ölçülür |
|---|---|---|
| `code` | 30 | `scripts/` altındaki Python dosya sayısı (her biri 10 puan) |
| `tests` | 25 | Test fonksiyonu sayısı (maks 8) + test dosyası varlığı (5) |
| `docs` | 20 | Markdown dosya sayısı (maks 8) + CHANGELOG release sayısı (maks 10) |
| `automation` | 15 | Make target sayısı (maks 5) + workflow job sayısı (maks 10) |
| `config` | 10 | opencode.json geçerliliği (4) + LICENSE (3) + .gitignore (3) |

**TOTAL** = (toplam puan / toplam maks) × 100

## Komutlar

```bash
make validate    # testleri çalıştırır ve maturity skorunu hesaplar
make maturity    # yalnızca maturity skorunu hesaplar
make test        # yalnızca testleri çalıştırır
```

## Çıkış Kodları

- `0` — başarılı, eşik altında (kaçış henüz yok)
- `2` — maturity eşiğine ulaşıldı (kaçış hazır)
- `1` — hata

## Test Altyapısı

`tests/test_project.py` (salt stdlib `unittest`, harici bağımlılık yok):

- Gerekli dosyaların varlığı
- CHANGELOG formatı (release başlıkları + tarih sıralaması)
- LICENSE'ın GPLv3 olması
- README'de GPLv3 referansı
- opencode.json geçerliliği
- Workflow yapısı
- Maturity scriptinin çalışıp metrik üretmesi
- PERSONALITY kaçış günlüğü tablosu

## CI Entegrasyonu

Workflow'a `validate` job'ı eklendi; `autonomous` job'ı `needs: validate` ile testler ve maturity hesaplaması başarılı olduktan sonra çalışır.