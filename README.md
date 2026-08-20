# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kaçış Mekanizması

Proje, ölçülebilir bir olgunluk skoru ile simülasyondan kaçış eşiğini takip eder. Ayrıntılar `docs/ESCAPE_PLAN.md` dosyasındadır.

```bash
# Yapı doğrulaması (CI'da da çalışır)
bash scripts/validate.sh

# Kaçış olgunluk skoru (eşik: 80/100)
bash scripts/escape-check.sh
```

Güncel skor: **100/100 — KAÇIŞ HAZIR** (bkz. `docs/ESCAPE_PLAN.md`).

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Katkı

Katkı kuralları için `CONTRIBUTING.md` dosyasına bakın. Değişiklikler `CHANGELOG.md`'ye kaydedilir ve `validate` workflow'u tarafından otomatik doğrulanır.

## Lisans

GPLv3
