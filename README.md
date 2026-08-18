# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Validation:** Proje yapısını doğrulayan otomatik kontroller (`make validate`)
- **Tests:** Test altyapısı — 17 test (`make test`)
- **CI:** Her push/PR'da validate + test çalıştıran GitHub Actions workflow
- **Maturity:** Kaçış/olgunluk skoru takibi (`make maturity`)

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirici Komutları

- `make validate` — proje yapısı kontrollerini çalıştırır
- `make test` — testleri çalıştırır
- `make maturity` — kaçış/olgunluk skorunu gösterir

## Lisans

GPLv3
