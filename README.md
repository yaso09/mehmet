# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Health Check:** Her push/PR'da `scripts/validate.sh` ile proje sağlığı doğrulanır
- **Kaçış Mekanizması:** PROGRESS.md'deki maturity skoru 80/100'e ulaşınca tetiklenir

## Kaçış Mekanizması / Escape Mechanism

mehmet, PROGRESS.md'de tanımlı ölçülebilir bir olgunluk skoru (maturity score)
üzerinden kaçış eşiğine ilerler. Skor her iterasyonda güncellenir ve
`scripts/validate.sh` ile doğrulanır. Mevcut skor için [PROGRESS.md](PROGRESS.md)'ye bakın.

## Geliştirme

- **Validation:** `bash scripts/validate.sh`
- **CI:** `.github/workflows/health-check.yml` her push/PR'da validation'ı çalıştırır

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
