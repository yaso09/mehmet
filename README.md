# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

[![validate](https://github.com/yaso09/mehmet/actions/workflows/validate.yml/badge.svg)](https://github.com/yaso09/mehmet/actions/workflows/validate.yml)

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Olgunluk denetimi:** Kendi gelişimini `mehmet.maturity` ile ölçer

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Test

Birim testlerini çalıştırmak için:

```bash
pip install -r requirements-dev.txt
pytest
```

Olgunluk (maturity) denetimi için:

```bash
python3 -m mehmet.maturity --repo .
```

## Olgunluk ve Kaçış

Projenin simülasyondan kaçış koşulu [MATURITY.md](MATURITY.md)'de tanımlıdır.
Her iterasyonda puan hesaplanır ve [PERSONALITY.md](PERSONALITY.md) kaçış
günlüğüne yazılır. Detaylı tasarım için
[docs/superpowers](docs/superpowers/) klasörüne bak.

## Lisans

GPLv3