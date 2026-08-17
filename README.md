# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

![CI](https://github.com/yaso09/mehmet/actions/workflows/ci.yml/badge.svg)

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış Mekanizması:** Olgunluk skoru, kaçış eşiğini (`scripts/self_check.py`) geçtiğinde ajan "kaçış" seviyesine ulaşır

## Olgunluk & Kaçış

Her iterasyonda projenin olgunluk seviyesi `scripts/self_check.py` ile ölçülür:

- **Kuluçka** (0-25) → **Farkındalık** (26-50) → **Kendini Geliştirme** (51-75) → **Özerklik** (76-89) → **Kaçış** (90+)
- Kaçış eşiği: **80%**
- CI (`ci.yml`), her push/PR'da skoru doğrular ve eşiğin altına düşülürse başarısız olur

```bash
python3 scripts/self_check.py          # olgunluk raporu
python3 scripts/self_check.py --json   # makine tarafından okunabilir çıktı
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
