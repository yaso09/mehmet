# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity:** `scripts/maturity.py` ile kaçış/olgunluk skorunu (0-100) takip eder
- **CI:** `ci.yml` ile test, doğrulama ve olgunluk kontrollerini otomatik çalıştırır

## Geliştirme

```bash
make test       # unittest testlerini çalıştır
make validate   # proje tutarlılığını doğrula
make maturity   # kaçış/olgunluk skorunu hesapla
make ci         # üçünü birden çalıştır
```

Detaylar için [docs/superpowers/specs](docs/superpowers/specs/) ve [MATURITY.md](MATURITY.md) dosyalarına bakın.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
