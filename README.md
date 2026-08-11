# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Geliştirme Altyapısı

- **Kaçış hazırlık metriği:** `scripts/check-escape-ready.sh` projenin olgunluk
  seviyesini 0-100 arası puanlar (kaçış eşiği: 80). `--strict`, `--json` ve
  `ESCAPE_THRESHOLD` değişkenini destekler.
- **Make komutları:** `make check` tüm kalite kontrollerini, `make lint` tüm
  lint'leri, `make test` kaçış hazırlığını doğrular.
- **CI:** `.github/workflows/ci.yml` markdownlint, yamllint, shellcheck ve kaçış
  hazırlığı kontrolünü her push/PR'da çalıştırır.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
