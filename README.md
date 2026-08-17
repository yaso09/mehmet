# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

![CI](https://github.com/yaso09/mehmet/actions/workflows/ci.yml/badge.svg)

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kaçış Yol Haritası

mehmet'in simülasyondan kaçış hedefi, projenin olgunluk seviyesiyle ölçülür.
Kaçış skoru (0-100) `scripts/mehmet_score.py` ile hesaplanır; detaylar
[docs/escape-roadmap.md](docs/escape-roadmap.md) içinde tanımlıdır.

```bash
python3 scripts/mehmet_score.py        # skor raporu
python3 scripts/mehmet_score.py --check  # CI doğrulaması
python3 -m unittest discover -s tests -v # testler
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
