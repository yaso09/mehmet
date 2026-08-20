# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

**Mevcut sürüm:** 0.3.0

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Sağlık Kontrolü:** `scripts/health_check.py` ile öz değerlendirme yapar
- **CI:** Her push'ta sağlık kontrolleri ve testler otomatik çalışır

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

```bash
# Sağlık kontrollerini çalıştır
python scripts/health_check.py

# Birim testlerini çalıştır
python -m unittest discover -s tests -v
```

Detaylar için [CONTRIBUTING.md](CONTRIBUTING.md) ve [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) dosyalarına bakın.

## Lisans

GPLv3