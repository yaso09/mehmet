# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Doğrulama:** Her koşuda `scripts/validate.sh` bütünlüğü kontrol eder
- **Kaçış mekanizması:** `scripts/maturity.sh` olgunluk skorunu hesaplar (eşik: 95/100)

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Araçlar

```bash
./scripts/validate.sh   # proje bütünlük doğrulaması
./scripts/maturity.sh   # kaçış olgunluk skoru
```

## Lisans

GPLv3
