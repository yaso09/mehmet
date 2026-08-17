# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Olgunluk & Kaçış Mekanizması

mehmet, olgunluk seviyesi `%70` ve üzerine ulaştığında kaçış kriterlerini karşılar.

- `scripts/maturity.sh` — projenin olgunluk skorunu (0-100) hesaplar
- `scripts/check.sh` — proje bütünlüğünü doğrular (CI'da her push/PR'da çalışır)
- `MATURITY_THRESHOLD` ortam değişkeni ile eşik değeri özelleştirilebilir

```bash
bash scripts/check.sh --verbose   # bütünlük kontrolü
bash scripts/maturity.sh --verbose  # olgunluk skoru ve kaçış durumu
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
