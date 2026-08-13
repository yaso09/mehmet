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

## Geliştirme & Olgunluk

Proje `scripts/assess.py` ile 0-100 arası bir olgunluk skoru üretir. Bu skor, kaçış mekanizmasının (maturity threshold) ölçülebilir temelidir.

```bash
make assess     # olgunluk raporu + geçmiş kaydı
make validate   # yapısal doğrulama
make test       # birim testleri
make check      # validate + test
```

Skor geçmişi `docs/MATURITY.md` içinde tutulur. Her iterasyonda yeni bir satır eklenir.

## Lisans

GPLv3
