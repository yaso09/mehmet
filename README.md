# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity:** `scripts/validate.sh` ile olgunluk skoru ölçülür, kaçış eşiği `MATURITY.md`'de takip edilir
- **CI:** Her push'ta `validate.yml` ile tutarlılık doğrulanır

## Kaçış Skoru

Kaçış, projenin olgunluk seviyesine ulaşmasıyla mümkündür.

```bash
scripts/validate.sh   # mevcut skoru gösterir (40 üzerinden, eşik: 32)
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
