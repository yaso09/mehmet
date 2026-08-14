# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity:** Kaçış hedefini ölçen olgunluk skorlama sistemi (`scripts/maturity.py`)

## Olgunluk / Kaçış Metriği

Proje, simülasyondan kaçışa ne kadar yaklaştığını `scripts/maturity.py` ile ölçer.
Skor beş boyutta (dokümantasyon, testler, otomasyon, kod kalitesi, repo hijyeni)
ağırlıklı olarak hesaplanır. Skor `80`'e ulaştığında proje kaçış eşiğini aşmış sayılır.

```bash
python3 scripts/maturity.py            # insan-okunur çıktı
python3 scripts/maturity.py --json     # makine-okunur çıktı (CI için)
```

## Geliştirme

```bash
python3 -m unittest discover -s tests -v   # testleri çalıştır
```

CI, her PR ve push'ta testleri çalıştırır ve maturity skorunu raporlar.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
