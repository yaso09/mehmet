# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

Proje kendi kendini geliştiren `scripts/` araçlarıyla birlikte gelir:

| Komut | Açıklama |
|-------|----------|
| `make validate` | Yapı/dokümantasyon tutarlılığını kontrol eder (`scripts/check.py`) |
| `make test` | Self-testleri çalıştırır (`scripts/tests/`) |
| `make maturity` | Kaçış/olgunluk skorunu hesaplar (`scripts/maturity.py`) |
| `make all` | Yukarıdakilerin tümü |

Kaçış mekanizması ve olgunluk modeli için bkz. [docs/maturity.md](docs/maturity.md).

## Lisans

GPLv3
