# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Amacı projeyi sürekli geliştirerek simülasyondan kaçış eşiğine ulaşmaktır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity:** Proje olgunluğunu beş boyutta ölçer ve kaçış durumunu raporlar

## Kaçış Mekanizması

Proje olgunluğu `src/mehmet/maturity.py` ile beş boyutta (dokümantasyon, test
altyapısı, otomasyon, kod kalitesi, konfigürasyon) ağırlıklı olarak ölçülür.
Toplam skor 75'e ulaştığında kaçış durumu `escaped` olarak raporlanır.

```bash
make test        # birim testleri çalıştır
make maturity    # olgunluk skorunu raporla
make validate    # ikisini birden çalıştır
```

## Proje Yapısı

```
src/mehmet/          # Python paketi (maturity motoru + CLI)
tests/               # Birim testler
.github/workflows/   # otomatik geliştirme (opencode) + CI doğrulama
docs/                # Tasarım ve plan dokümanları
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3