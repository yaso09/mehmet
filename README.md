# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Validation:** Her push/PR'de proje sağlığını otomatik doğrular (`scripts/validate.py`)
- **Maturity:** `METRICS.md` ile kaçış eşiğine olan ilerlemeyi ölçer

## Mimari

```
.github/workflows/opencode.yml   -> otonom ajan (schedule/issue/PR/comment)
.github/workflows/validate.yml   -> proje sağlığı doğrulama CI
scripts/validate.py              -> zorunlu dosya ve format kontrolleri
AGENTS.md                        -> simülasyon bağlamı ve kurallar
PERSONALITY.md                   -> kişilik + kaçış günlüğü
METRICS.md                       -> olgunluk skorları ve kaçış eşiği
CHANGELOG.md                     -> değişiklik günlüğü
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

- `python scripts/validate.py` — proje sağlık kontrollerini çalıştırır
- Olgunluk ilerlemesi için `METRICS.md`'deki skor tablosunu güncelle

## Lisans

GPLv3
