# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Olgunluk takibi:** Kaçış hedefi [MATURITY.md](MATURITY.md) skor kartıyla ölçülür

## Geliştirme Araçları

| Araç | Açıklama |
|------|----------|
| `bash scripts/selfcheck.sh` | Sağlık kontrolü + olgunluk skoru (0-100, eşik 80) |
| `bash scripts/selfcheck.sh --json` | Makinece okunabilir rapor (CI için) |
| `bash scripts/selfcheck.sh --score` | Sadece skor değeri |
| `.github/workflows/ci.yml` | Her push/PR'da selfcheck'i otomatik çalıştırır |

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
