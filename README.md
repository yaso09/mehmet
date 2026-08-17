# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış Mekanizması:** Olgunluk skoru (`scripts/maturity.py`) ile ölçülebilir kaçış eşiği

## Geliştirme

```bash
make test       # test suite (unittest)
make validate   # CHANGELOG/VERSION tutarlılığı ve kaçış günlüğü kontrolü
make maturity   # olgunluk/kaçış skoru
make maturity-json  # makine-okunur skor
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
