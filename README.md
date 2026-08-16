# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity:** `scripts/maturity.py` ile ölçülebilir olgunluk skoru hesaplar

## Kaçış Eşiği

Olgunluk skoru 0-100 arasında hesaplanır. Kaçış, skorun **≥80** olup üst üste **3 ardışık çalıştırmada** korunmasıyla tetiklenir. Kriterler ve rapor formatı için [MATURITY.md](MATURITY.md) dosyasına bak.

```bash
python3 scripts/maturity.py                 # skoru hesapla, raporu yaz
python3 -m unittest discover -s tests -v    # testleri çalıştır
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
