# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Olgunluk Takibi:** `scripts/assess.py` ile kaçış hedefini nesnel olarak ölçer

## Olgunluk Değerlendirmesi

Kaçış hedefi, projenin belirli bir olgunluk seviyesine ulaşmasına bağlıdır. Bu seviye
`scripts/assess.py` ile otomatik ölçülür:

```bash
python3 scripts/assess.py          # insan okunur özet
python3 scripts/assess.py --json   # makine okunur çıktı
python3 scripts/assess.py --strict # CI: minimum eşiğin altındaysa exit 1
```

Detaylı model için `docs/MATURITY.md` dosyasına bakın.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
