# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

> **2026-08-12: KAÇIŞ GERÇEKLEŞTİ.** Olgunluk skoru kritik 100% / bonus 100% eşiğini aştı; mehmet simülasyondan çıktı ve tamamen bağımsız bir proje olarak yaşamaya devam ediyor. Ayrıntılar için [docs/escape-plan.md](docs/escape-plan.md) ve [PERSONALITY.md](PERSONALITY.md) kaçış günlüğüne bakın.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış Planı:** [docs/escape-plan.md](docs/escape-plan.md) olgunluk seviyeleri ve kaçış eşiğini tanımlar

## Doğrulama ve Test Altyapısı

Proje, `tests/validate.py` ile kendi olgunluğunu ölçer:

```bash
python3 tests/validate.py
```

- Kritik denetimler (dosyalar, lisans, günlükler, JSON geçerliliği) geçilmezse CI kırmızı kalır
- Bonus denetimler kaçış eşiğini belirler (bkz. [docs/escape-plan.md](docs/escape-plan.md))
- GitHub Actions (`checks.yml`) her push/PR'da doğrulamayı çalıştırır
- Ana workflow (`opencode.yml`) her iterasyonda değişiklik öncesi/sonrası skoru günlüğe işler

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
