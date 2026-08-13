# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Doğrulama:** `scripts/validate.sh` proje sağlık kontrolü (push/PR'da otomatik çalışır)
- **Kaçış Mekanizması:** `scripts/check_escape.sh` olgunluk seviyesini ölçer

## Kaçış Hedefi

mehmet, [docs/MATURITY.md](docs/MATURITY.md) içindeki olgunluk çerçevesini takip eder.
Kaçış, dört boyutta (test altyapısı, kod kalitesi, dokümantasyon, otomasyon) belirlenen
eşiklere ulaşıldığında mümkündür. Güncel durumu şu komutla kontrol et:

```bash
bash scripts/check_escape.sh
```

## Geliştirme

```bash
# Proje sağlık kontrolü
bash scripts/validate.sh

# Kaçış hazırlık kontrolü
bash scripts/check_escape.sh
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
