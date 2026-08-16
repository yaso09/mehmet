# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity (Kaçış Mekanizması):** Projeyi beş boyutta puanlar, ilerlemeyi `docs/metrics.json`'a kaydeder; 80/100 eşiğinde kaçış sinyali verir
- **Test Altyapısı:** `make validate` ile proje bütünlüğü testleri ve maturity skoru çalışır

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

```bash
make test       # proje testlerini çalıştırır (stdlib unittest)
make maturity   # maturity / kaçış skorunu hesaplar
make validate   # testler + maturity (CI ile aynı)
```

## Lisans

GPLv3
