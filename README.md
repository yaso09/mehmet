# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış Mekanizması:** `scripts/maturity.py` ile ölçülen olgunluk skoru ve seviye eşikleri (bkz. `MATURITY.md`)
- **Test Altyapısı:** `tests/` dizinindeki `pytest` testleri proje tutarlılığını doğrular
- **CI:** `push`/`PR` üzerinde test ve olgunluk kontrolü çalıştıran GitHub Actions workflow'u

## Geliştirme

```bash
# Testleri çalıştır
python -m pytest -v

# Olgunluk skorunu hesapla
python scripts/maturity.py

# MATURITY.md dosyasını güncelle
python scripts/maturity.py --write
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
