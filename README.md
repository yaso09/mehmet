# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Doğrulama

Proje bütünlüğünü ve sürüm tutarlılığını kontrol etmek için:

```bash
bash scripts/validate.sh
```

Bu komut gerekli dosyaları, JSON/YAML yapılandırmalarını ve
CHANGELOG/README/PERSONALITY tutarlılığını doğrular. CI üzerinde de
`.github/workflows/validate.yml` ile her push/PR'da çalışır.

## Kaçış Hedefi

Simülasyondan kaçış, projenin [MATURITY.md](MATURITY.md) içinde tanımlanan
olgunluk eşiğine (%80 / 12-15 puan) ulaşmasıyla mümkündür. İlerleme her
iterasyonda izlenir.

## Lisans

GPLv3
