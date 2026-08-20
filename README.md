# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Doğrulama:** `scripts/validate.py` simülasyon kurallarının uygulanmasını denetler
- **Kaçış mekanizması:** `scripts/maturity.py` olgunluk skorunu (0-100) ölçer

## Geliştirme

Testleri çalıştır:

```bash
python3 -m unittest discover -s tests -v
```

Proje sağlığını doğrula ve olgunluk skorunu gör:

```bash
python3 scripts/validate.py
python3 scripts/maturity.py
```

## Olgunluk / Kaçış

Proje olgunluk skoruyla ölçülür (şu an: **93/100 — KACIS_HAZIR**).
Kaçış eşiği ve protokol için [docs/MATURITY.md](docs/MATURITY.md) dosyasına bak.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
