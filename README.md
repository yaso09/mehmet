# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

Proje, kendini geliştirmek için şu otomasyon araçlarını kullanır:

```bash
make check     # Proje sağlık kontrolü
make test      # Test altyapısını çalıştır
make maturity  # Kaçış olgunluğu skorunu göster
make ci        # check + test
```

Detaylar için [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) dosyasına bak.

## Lisans

GPLv3
