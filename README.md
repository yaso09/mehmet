# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış Mekanizması:** `scripts/check.sh` ile ölçülen olgunluk skoru (0-100)

## Olgunluk / Kaçış

Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkündür.
Ayrıntılar için [MATURITY.md](MATURITY.md) dosyasına bakın.

Ölçüm:

```bash
scripts/check.sh
```

- Skor **>= 80** → OLGUN (kaçış eşiği karşılandı)
- Skor **< 80** → GELİŞMEKTE (iterasyona devam edilir)

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
