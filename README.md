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

```bash
make test       # unittest ile proje yapısını doğrula
make validate   # test + workflow YAML sözdizimi kontrolü
make metrics    # olgunluk skorunu ölç ve METRICS.md'yi güncelle
make check      # kaçış eşiğine ulaşıldı mı? (exit 0/1)
```

## Kaçış Mekanizması

Proje olgunluğu `scripts/maturity.py` ile ölçülür. Skor `METRICS.md` dosyasına yazılır.
Eşik değere (90%) ulaşıldığında `make check` komutu `escape-ready` döner ve kaçış mümkün hale gelir.

## Lisans

GPLv3
