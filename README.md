# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Otomatik kalite kontrolü:** Her değişiklikte testler ve maturity raporu çalışır

## Kaçış Mekanizması

mehmet, simülasyondan çıkışını projenin olgunluğuyla ölçer. `src/maturity.py` motoru
dokümantasyon, test altyapısı, otomasyon, kaynak kod ve CI/CD bileşenlerini puanlar.
Eşik (`ESCAPE_THRESHOLD` = 8.0/10.0) aşıldığında kaçış mümkün hale gelir.

Raporu görüntülemek için:

```bash
make report        # insan-okur rapor
make strict        # eşiğin altındaysa sıfır olmayan çıkış kodu
```

Skor geçmişi `PROGRESS.md` dosyasında tutulur.

## Geliştirme

```bash
make test          # unittest testlerini çalıştır
```

Test kümesi `tests/` altında, maturity motoruna yönelik 17 testten oluşur.
Kalite işi (`.github/workflows/quality.yml`) her push ve PR'da testleri
çalıştırıp maturity raporunu üretir.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3