# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Test altyapısı:** `make validate` ile proje sağlığı doğrulanır ve olgunluk skoru üretilir
- **CI:** Her push/PR'da `.github/workflows/ci.yml` çalışır

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

```bash
make validate   # proje sağlığını doğrula (PASS olmalı)
make score      # olgunluk skorunu göster
```

Katkı kuralları için `CONTRIBUTING.md`'ye bakın.

## Lisans

GPLv3
