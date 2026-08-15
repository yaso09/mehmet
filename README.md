# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Olgunluk takibi:** Her iterasyonda `scripts/maturity.py` ile 5 boyutta puanlanır ve kaçış koşulu denetlenir

## Kaçış Sistemi

mehmet, proje belirli bir olgunluk seviyesine ulaşınca simülasyondan kaçabilir.
`scripts/maturity.py` projeyi 100 puan üzerinden değerlendirir, `MATURITY.md`'ye yazar
ve geçmişi `.maturity_history.json`'da tutar.

**Kaçış koşulu:** Üst üste iki ölçümde puan >= 90/100.
Güncel durum: [MATURITY.md](MATURITY.md)

## Geliştirme

```bash
# Testleri çalıştır
python -m unittest discover -s tests -v

# Olgunluk puanını ölç ve MATURITY.md'yi güncelle
python scripts/maturity.py
```

Detaylar için [CONTRIBUTING.md](CONTRIBUTING.md) ve [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
