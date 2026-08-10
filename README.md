# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI Gate:** Her çalışmadan önce `tests/verify.py` ile bütünlük testi çalışır
- **Kaçış Metrikleri:** Olgunluk skoru `docs/kaçış-metrikleri.md` ile takip edilir

## Geliştirme

```bash
make test      # bütünlük testlerini çalıştır
python3 bin/mehmet-status.py       # durum raporu
python3 bin/mehmet-status.py --score  # kaçış skoru (0-100)
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
