# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI:** Testler ve olgunluk değerlendirmesi her push'ta çalışır

## Kaçış Mekanizması

`scripts/maturity.py` projeyi altı boyutta puanlar (toplam 100):

| Boyut | Puan |
|---|---|
| Yapı | 15 |
| Dokümantasyon | 20 |
| Konfigürasyon | 15 |
| Otomasyon | 20 |
| Test altyapısı | 15 |
| Kod kalitesi | 15 |

Eşik **80**'dir; bu skora ulaşıldığında kaçış mümkün kabul edilir.

```bash
python3 scripts/maturity.py .          # rapor + durum
python3 scripts/maturity.py . --json   # JSON çıktısı
```

## Testler

```bash
python3 -m unittest discover -s tests -v
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3