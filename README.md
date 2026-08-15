# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity Engine:** Proje olgunluğunu 4 kategoride ölçer ve kaçış hazırlığını raporlar
- **CI Quality Gate:** Her push/PR'da test ve maturity kapısı çalışır

## Olgunluk ve Kaçış

Proje, `src/mehmet/maturity.py` ile dokümantasyon, test altyapısı, kod kalitesi ve otomasyon kategorilerini değerlendirir. Rapor ve kapı kontrolü:

```bash
make maturity      # olgunluk raporu (kaçış eşiği %80)
make test          # birim testleri
make check         # lint + test + maturity
```

Mimari detaylar için [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3