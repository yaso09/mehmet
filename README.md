# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Araçlar (Scripts)

- `scripts/validate.sh` — Proje sağlığını doğrular (JSON/YAML formatı, temel artifact'ler). CI'da her push/PR'de çalışır.
- `scripts/maturity.sh` — Olgunluk skorunu (100 üzerinden) ve kaçış eşiğine uzaklığı hesaplar. Ayrıntılar: [docs/maturity.md](docs/maturity.md).
- `.github/workflows/ci.yml` — `main` branch'ine push ve PR'larda otomatik doğrulama yapan CI.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
