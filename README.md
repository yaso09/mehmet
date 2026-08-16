# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Doğrulama (Validation)

Proje bütünlüğü her push ve PR'da otomatik doğrulanır:

```bash
bash scripts/validate.sh
```

Bu script dosya bütünlüğünü, `opencode.json` schema uyumluluğunu, CHANGELOG ve PERSONALITY formatını kontrol eder. GitHub Actions'ta `validate.yml` workflow'u olarak da çalışır.

## Olgunluk Metrikleri

Kaçış hedefine giden yol, [MATURITY.md](MATURITY.md) içindeki olgunluk puanı ile ölçülür. Puan; kod kalitesi, test altyapısı, dokümantasyon ve otomasyon kategorilerinde toplanır.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
