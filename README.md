# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış Mekanizması:** Proje olgunluğunu nesnel olarak ölçer ve kaçış eşiğini (95/100) izler

## Kaçış Mekanizması (Olgunluk Ölçümü)

mehmet, simülasyondan kaçış için proje olgunluğunu 5 boyutta (structure,
documentation, code, tests, automation) ölçer. Detaylar: [docs/maturity.md](docs/maturity.md).

```bash
make maturity                 # İnsan-okur rapor
python -m mehmet --json       # Makine-okur JSON rapor
```

## Geliştirme

```bash
pip install pytest
make test                     # Testleri çalıştır
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
