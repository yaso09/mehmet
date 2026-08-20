# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kalite Kapısı:** Her push'ta test suite ve maturity kontrolü otomatik çalışır
- **Maturity Sistemi:** Projenin kaçış hedefine yaklaşımını 0-100 arası ölçer

## Test ve Kalite

Testler standart kütüphane ile yazılmıştır (harici bağımlılık yok):

```bash
make test       # test suite'ini çalıştırır
make maturity   # maturity skorunu gösterir
make check      # test + maturity birlikte
make lint       # sözdizimi kontrolü
```

Maturity sistemi 5 boyutu ölçer: `docs`, `automation`, `tests`, `quality`, `resilience`. Detaylı JSON çıktısı için:

```bash
python scripts/maturity.py --json
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
