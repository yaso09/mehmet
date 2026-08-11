# mehmet

Kendi kendisini geliştiren otonom AI ajan.

**Version:** 0.3.0

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI Validation:** Her push/PR'da `scripts/validate.sh` ile proje yapısını doğrular
- **Maturity Tracker:** `MATURITY.md` ile kaçış/olgunluk ilerlemesini ölçer

## Proje Yapısı

- `AGENTS.md` — Simülasyon bağlamı ve ajan kuralları
- `PERSONALITY.md` — Kişilik evrimi ve kaçış günlüğü
- `MATURITY.md` — Olgunluk/kaçış eşiği takipçisi
- `VERSION` — Sürüm kaynağı (source of truth)
- `CHANGELOG.md` — Değişiklik günlüğü
- `scripts/validate.sh` — Otomatik yapı doğrulama
- `.github/workflows/` — Otomasyon (opencode + validate)

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

Her iterasyonda sürümü `VERSION` dosyasında artır ve değişiklikleri `CHANGELOG.md`'ye ekle.

## Lisans

GPLv3
