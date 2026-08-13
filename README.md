# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity:** Her çalışmada olgunluk skoru (0-100) ve testler çalıştırılır

## Kaçış Mekanizması

mehmet, projenin olgunluk seviyesini `scripts/maturity.py` ile ölçer. Skor 85'e
ulaştığında kaçış adayı ilan edilir. Skor; kod, test, dokümantasyon, otomasyon,
konfigürasyon, governance, öz-farkındalık ve sürüm takibi boyutlarından hesaplanır.

```bash
python3 scripts/maturity.py          # skor raporu
python3 -m unittest discover -s scripts -p "test_*.py"   # testler
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
