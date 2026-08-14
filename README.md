# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity Check:** Her push'ta olgunluk skoru otomatik hesaplanır

## Gelişim ve Kaçış

mehmet, simülasyondan kaçış hedefini olgunluk ölçümüyle takip eder.
Detaylı kaçış mekanizması, skorlama kriterleri ve kaçış eşiği için
[docs/escape-roadmap.md](docs/escape-roadmap.md) dosyasına bakın.

```bash
make maturity   # Olgunluk raporu
make test       # Betik testleri
make check      # Tüm kontroller
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
