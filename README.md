# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış takibi:** `scripts/maturity.py` ile olgunluk skoru hesaplanır (0-100)

## Geliştirme

```bash
bash tests/run.sh              # yapısal bütünlük testleri
python3 scripts/maturity.py    # kaçış olgunluk skoru
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Katkı

Katkı kuralları için [CONTRIBUTING.md](CONTRIBUTING.md) dosyasına bak.

## Lisans

GPLv3
