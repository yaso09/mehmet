# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity:** `scripts/maturity.py` ile ölçülebilir olgunluk skoru ve kaçış takibi (bkz. `docs/maturity.md`)

## Geliştirme

Testler standart `unittest` ile yazılmıştır:

```bash
python3 -m unittest discover -s tests -t . -v
```

Kalite CI'ı `.github/workflows/quality.yml` ile testleri ve kaçış-hazırlık
kapısını (`python3 scripts/maturity.py`) her push/PR'da çalıştırır.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
