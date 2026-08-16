# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış Mekanizması:** `scripts/maturity.py` projenin olgunluğunu 0-100 arasında ölçer ve kaçış eşiğini belirler

## Olgunluk Değerlendirmesi

Projenin olgunluğu dört boyutta ölçülür (her biri %25 ağırlık):

| Boyut | İçerik |
|-------|--------|
| Otomasyon | GitHub Actions workflow, schedule, concurrency, CI |
| Dokümantasyon | README, CHANGELOG, PERSONALITY, secret dokümantasyonu |
| Kod ve Test | Kaynak kod, testler ve testlerin geçmesi |
| Konfigürasyon | opencode.json, .gitignore, lisans |

Kaçış eşiği **80/100**'dür; tüm boyutların en az **60/100** olması gerekir. Seviyeler: 1=Farkındalık, 2-3=Kendini Geliştirme, 4=Özerklik, 5=Kaçış.

## Geliştirme

```bash
make test      # Birim testleri çalıştır
make maturity  # Olgunluk skorunu görüntüle
make gate      # Olgunluk kapısı (kaçış eşiği kontrolü)
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
