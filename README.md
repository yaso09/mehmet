# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kaçış Mekanizması

mehmet, projenin olgunluk seviyesini ölçerek kaçış kriterini takip eder:

- **Olgunluk ölçümü:** `scripts/check-project.sh` (0-100 skor, 80+ = kaçış kriteri)
- **Test altyapısı:** `tests/test-check-project.sh` ile doğrulanır
- **Kalite kapısı:** `.github/workflows/validate.yml` her push/PR'da kontrol eder
- **Tek komut:** `make validate` (strict kontrol + testler + shellcheck)

## Geliştirme

```bash
make check          # Olgunluk raporu
make check-strict   # Strict olgunluk kontrolü (kalite kapısı)
make test           # Testleri çalıştır
make validate       # Tüm doğrulamaları çalıştır
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
