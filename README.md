# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Test altyapısı:** Proje bütünlüğünü doğrulayan `unittest` tabanlı testler
- **Kaçış ölçümü:** `scripts/maturity.py` ile kaçış olgunluğunu skorlar

## Testler

Proje bütünlüğünü doğrulayan Python `unittest` testleri `tests/` altındadır:

```bash
python3 -m unittest discover -s tests -v
```

Her iterasyonda CI (`validate` job) testleri ve kaçış ölçümünü çalıştırır.

## Kaçış / Olgunluk Skoru

`scripts/maturity.py` projeyi 5 boyutta skorlar: dokümantasyon, test
altyapısı, otomasyon, kod kalitesi ve kendini geliştirme. Skor `80`
eşiğini geçtiğinde proje kaçış için olgun kabul edilir.

```bash
python3 scripts/maturity.py          # skoru göster
python3 scripts/maturity.py --json   # makine okunabilir çıktı
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
