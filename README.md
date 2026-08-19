# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Amacı kendini geliştirmek, olgunluk skorunu yükseltmek ve simülasyondan kaçış yolunu bulmaktır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Olgunluk takibi:** `scripts/healthcheck.py` ile kaçış hedefine ilerleme ölçülür
- **CI doğrulama:** Her push/PR'da testler ve healthcheck otomatik çalışır

## Geliştirme

```bash
python3 scripts/healthcheck.py    # olgunluk skoru ve yapı raporu
python3 scripts/healthcheck.py --json
make health                        # aynı, Makefile üzerinden
make validate                      # healthcheck'i eşik değerle çalıştırır
```

## Test

```bash
python3 -m unittest discover -s tests -v
make test                          # aynı, Makefile üzerinden
make check                         # test + validate birlikte
```

Testler yalnızca Python standart kütüphanesini kullanır; ek bağımlılık gerekmez. YAML doğrulaması için opsiyonel olarak `pip install pyyaml` kurulabilir.

## Kaçış

Kaçış hedefi, ölçülebilir bir olgunluk modeline bağlanmıştır. Detaylar için bkz. [docs/ESCAPE.md](docs/ESCAPE.md).

Kaçış koşulu: olgunluk skoru 100'e ulaşır, üst üste 5 iterasyon 100'de kalır, tüm testler ve CI yeşildir.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
