# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity scoring:** `scripts/maturity.sh` ile 0-100 olgunluk skoru hesaplar, kaçış eşiği %80 (`--gate`)
- **Self-test:** `tests/test-project.sh` ile kural uyumunu doğrular
- **CI validation:** `.github/workflows/validate.yml` push/PR'da test ve skoru çalıştırır
- **Kaçış planı:** `docs/escape-plan.md` ile simülasyondan çıkış mekanizmasını tanımlar

## Kaçış / Escape

Kaçış, projenin belirli bir olgunluk seviyesine (%80) art arda 3 iterasyon ulaşmasıyla
tetiklenir. Detaylar için [docs/escape-plan.md](docs/escape-plan.md) bölümünü inceleyin.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
