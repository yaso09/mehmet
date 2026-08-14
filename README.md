# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Olgunluk skoru:** `scripts/maturity.py` ile kaçış eşiğini (75/100) ölçer
- **CI doğrulama:** Her push/PR'da `validate.yml` bütünlük, test ve kalite kontrolleri yapar

## Geliştirme

```bash
make check      # validate + test
make maturity   # olgunluk skoru raporu
make ci         # check + maturity (CI ile aynı)
make clean      # geçici dosyaları temizle
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
