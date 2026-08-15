# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Olgunluk mekanizması:** Her iterasyonda repo sağlığı ölçülür, kaçış eşiği takip edilir

## Olgunluk ve Kaçış Mekanizması

mehmet, her iterasyonda `scripts/health-check.sh` ile repo sağlığını ölçer ve 0-100 arasında olgunluk skoru üretir. Skor 80 ve üzeri ise proje kaçış eşiğine ulaşmış sayılır.

```bash
make check   # sağlık kontrolü + olgunluk skoru
make score   # yalnızca skor
make json    # makine-okunabilir JSON raporu
make help    # tüm hedefler
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

- Yapılan her değişiklik `CHANGELOG.md`'ye eklenir
- Kişilik ve kaçış günlüğü `PERSONALITY.md`'de tutulur
- Tasarım kararları `docs/superpowers/` altında saklanır

## Lisans

GPLv3
