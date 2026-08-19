# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Self-check:** CI'da proje bütünlüğünü doğrular ve olgunluk skorunu hesaplar

## Test

Proje bütünlüğünü doğrulamak için:

```bash
python3 scripts/self_check.py        # standart kosum
python3 scripts/self_check.py --strict  # uyarilari da hata sayar
```

Test, `.github/workflows/opencode.yml` içindeki `self-check` job'ı ile her
tetiklemede CI'da otomatik çalışır.

## Olgunluk ve Kaçış

Olgunluk seviyesi ve kaçış kriterleri [MATURITY.md](MATURITY.md) içinde takip edilir.
Kaçış günlüğü [PERSONALITY.md](PERSONALITY.md) içinde tutulur.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
