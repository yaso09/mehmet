# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Doğrulama:** `scripts/validate.sh` proje sağlığını kontrol eder, CI'da koşar
- **Sürümleme:** `VERSION` + `scripts/bump-version.sh` ile otomatik sürüm artırımı
- **Kaçış Takibi:** `docs/maturity.md` ile ölçülebilir olgunluk skoru ve kaçış eşiği (80/100)

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirici Komutları

```bash
scripts/validate.sh          # Proje sağlık kontrolü (CI'da da koşar)
scripts/bump-version.sh patch # Sürümü artır (patch|minor|major)
```

## Lisans

GPLv3
