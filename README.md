# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Geliştirme

Proje, kod kalitesi ve kaçış hedefini izlemek için otomasyon araçları içerir:

```bash
make test       # Proje bütünlüğü testlerini çalıştırır
make maturity   # Olgunluk skorunu hesaplar ve rapor üretir
make verify     # Testleri çalıştırır + olgunluk raporunu üretir
```

- `tests/` — Proje yapısını doğrulayan `unittest` testleri
- `scripts/maturity.py` — Kaçış eşiğini (80/100) ölçen olgunluk skorlayıcı
- `docs/maturity-report.md` — Otomatik üretilen olgunluk raporu
- CI, her değişiklikte test job'ını çalıştırır

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
