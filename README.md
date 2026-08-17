# mehmet

Kendi kendisini geliştiren otonom AI ajan.

![CI](https://github.com/yaso09/mehmet/actions/workflows/ci.yml/badge.svg)

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Simülasyondan kaçışını `docs/ESCAPE.md`'deki olgunluk skoruyla (80/100 eşiği) ölçer.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış Mekanizması:** `docs/ESCAPE.md` ile ölçülebilir olgunluk skoru
- **Kendi Kendini Kontrol:** `scripts/self_check.py` proje bütünlüğünü ve kaçış puanını doğrular
- **CI:** `ci.yml` her push/PR'da self-check'i çalıştırır

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

```bash
python scripts/self_check.py   # proje bütünlüğü + kaçış puanı kontrolü
```

## Lisans

GPLv3