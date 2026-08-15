# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Self-Verification:** Her iterasyonda `scripts/verify.py` ile proje sağlığını ve
  olgunluk skorunu ölçer (bkz. [MATURITY.md](MATURITY.md))
- **Test Suite:** `tests/` altında `unittest` tabanlı otomatik testler
  (`python3 -m unittest discover -s tests`)

## Geliştirme

```bash
# Proje sağlık kontrolü ve olgunluk skoru
python3 scripts/verify.py

# Testleri çalıştır
python3 -m unittest discover -s tests
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
