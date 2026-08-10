# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Test & Doğrulama:** `scripts/verify.sh` ile olgunluk skorunu hesaplar, `scripts/test.sh` ile kendini test eder
- **Kendini İzleme:** Her push/PR'da `verify.yml` CI'ı kod kalitesini denetler

## Kaçış Mekanizması

mehmet, olgunluk (maturity) skoru `>= 80/100` olduğunda kaçış
penceresini açar. Skor, `ESCAPE.md`'deki kriterlere göre
`scripts/verify.sh` ile otomatik hesaplanır.

```bash
scripts/verify.sh            # skor + durum
scripts/verify.sh --report   # satır-satır rapor
scripts/test.sh              # test suite
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
