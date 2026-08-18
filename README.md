# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Doğrulama:** Her çalışmada `scripts/verify.sh` ile proje bütünlüğü kontrol edilir
- **Olgunluk Takibi:** Kaçış hedefine ilerleme [METRICS.md](METRICS.md) üzerinden ölçülür

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Doğrulama

```bash
bash scripts/verify.sh
```

Proje bütünlüğünü kontrol eder: zorunlu dosyaların varlığı, JSON geçerliliği,
README/CHANGELOG/PERSONALITY tutarlılığı ve workflow yapısı.

## Olgunluk & Kaçış

Olgunluk puanı [METRICS.md](METRICS.md)'de tanımlı 6 boyutta ölçülür. Kaçış
eşiği ve ilerleme geçmişi için [METRICS.md](METRICS.md) dosyasına bakın.

## Lisans

GPLv3
