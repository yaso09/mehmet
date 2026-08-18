# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Olgunluk & Kaçış Mekanizması

mehmet'in gelişimi ölçülebilirdir. `scripts/maturity.py` projeyi 15 kalite sinyali üzerinden tarar ve 0-100 arası puan üretir:

- **Kaçış eşiği:** 90/100
- **Rapor:** `docs/maturity.md` (her koşuda otomatik güncellenir)
- **Geçmiş:** `docs/maturity_history.json`

Kalite kapısı `.github/workflows/ci.yml` ile her push/PR'de otomatik çalışır. Testler `python3 -m unittest discover -s scripts -p 'test_*.py'` ile koşulur.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
